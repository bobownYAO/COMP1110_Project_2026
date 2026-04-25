from __future__ import annotations

import argparse
import csv
import random
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class GenerationConfig:
	strategy: str
	strategy_label: str
	restaurant_count: int
	customers_per_restaurant: int
	vip_probability: float
	group_probabilities: tuple[float, float, float]
	arrival_gap_mode: str
	arrival_gaps: tuple[int, ...]


TABLE_SIZE_DEFS = [
	("A", (8, 14)),
	("B", (4, 10)),
	("C", (3, 5)),
]
STRATEGY_ALIASES = {
	"single": ("single_snake", "single"),
	"single_snake": ("single_snake", "single"),
	"size_base": ("size_base", "size_base"),
	"size": ("size_base", "size_base"),
	"vip": ("vip", "vip"),
}
BASELINE_VIP_PROBABILITY = 0.20
BASELINE_GROUP_PROBABILITIES = (0.60, 0.20, 0.20)
ARRIVAL_GAP_DISTRIBUTIONS = {
	"long": (2, 3, 5, 7, 10, 12, 15, 20),
	"normal": (0, 0, 1, 1, 2, 3, 5, 7),
	"short": (0, 0, 0, 0, 1, 1, 2, 3),
}


def _write_csv(file_path: Path, rows: list[dict], columns: list[str]) -> None:
	file_path.parent.mkdir(parents=True, exist_ok=True)
	with file_path.open("w", newline="", encoding="utf-8") as f:
		writer = csv.DictWriter(f, fieldnames=columns)
		writer.writeheader()
		writer.writerows(rows)


def _parse_probability(value: str) -> float:
	cleaned = value.strip()
	if cleaned.endswith("%"):
		number = float(cleaned[:-1].strip()) / 100
	else:
		number = float(cleaned)
		if number > 1:
			number /= 100

	if not 0 <= number <= 1:
		raise ValueError("Probability must be between 0 and 1, or between 0% and 100%.")
	return number


def _prompt_yes_no(prompt: str, default: bool = True) -> bool:
	suffix = "[Y/n]" if default else "[y/N]"
	while True:
		answer = input(f"{prompt} {suffix}: ").strip().lower()
		if not answer:
			return default
		if answer in {"y", "yes"}:
			return True
		if answer in {"n", "no"}:
			return False
		print("Please enter Y or N.")


def _prompt_int(prompt: str, min_value: int = 1) -> int:
	while True:
		answer = input(f"{prompt}: ").strip()
		try:
			value = int(answer)
		except ValueError:
			print("Please enter an integer.")
			continue

		if value < min_value:
			print(f"Please enter an integer >= {min_value}.")
			continue
		return value


def _prompt_probability(prompt: str) -> float:
	while True:
		answer = input(f"{prompt}: ").strip()
		try:
			return _parse_probability(answer)
		except ValueError as exc:
			print(f"Invalid probability: {exc}")


def _prompt_strategy() -> tuple[str, str]:
	while True:
		answer = input("Strategy (single / size_base / vip): ").strip().lower()
		answer = answer.replace("-", "_")
		if answer in STRATEGY_ALIASES:
			return STRATEGY_ALIASES[answer]
		print("Invalid strategy. Please choose single, size_base, or vip.")


def _prompt_group_probabilities() -> tuple[float, float, float]:
	if _prompt_yes_no(
		"Use baseline group-size distribution A=60%, B=20%, C=20%?",
		default=True,
	):
		return BASELINE_GROUP_PROBABILITIES

	while True:
		answer = input(
			"Enter custom A and B probabilities, separated by comma "
			"(for example: 60,20 or 0.6,0.2): "
		).strip()
		parts = [part for part in re.split(r"[\s,]+", answer) if part]
		if len(parts) != 2:
			print("Please enter exactly two values: A probability and B probability.")
			continue

		try:
			a_probability = _parse_probability(parts[0])
			b_probability = _parse_probability(parts[1])
		except ValueError as exc:
			print(f"Invalid probability: {exc}")
			continue

		c_probability = 1 - a_probability - b_probability
		if c_probability < 0:
			print("A + B cannot be greater than 100%. Please try again.")
			continue
		return a_probability, b_probability, c_probability


def _prompt_arrival_gap_mode() -> tuple[str, tuple[int, ...]]:
	while True:
		answer = input("Arrival time interval (long / normal / short): ").strip().lower()
		if answer in ARRIVAL_GAP_DISTRIBUTIONS:
			return answer, ARRIVAL_GAP_DISTRIBUTIONS[answer]
		print("Invalid interval mode. Please choose long, normal, or short.")


def collect_config() -> GenerationConfig:
	strategy, strategy_label = _prompt_strategy()

	if strategy == "vip":
		if _prompt_yes_no("Use baseline VIP probability = 20%?", default=True):
			vip_probability = BASELINE_VIP_PROBABILITY
		else:
			vip_probability = _prompt_probability("VIP occurrence probability")
	else:
		vip_probability = 0.0

	restaurant_count = _prompt_int("Number of restaurants", min_value=1)
	customers_per_restaurant = _prompt_int("Total customers per restaurant", min_value=1)
	group_probabilities = _prompt_group_probabilities()
	arrival_gap_mode, arrival_gaps = _prompt_arrival_gap_mode()

	return GenerationConfig(
		strategy=strategy,
		strategy_label=strategy_label,
		restaurant_count=restaurant_count,
		customers_per_restaurant=customers_per_restaurant,
		vip_probability=vip_probability,
		group_probabilities=group_probabilities,
		arrival_gap_mode=arrival_gap_mode,
		arrival_gaps=arrival_gaps,
	)


def _generate_restaurants(
	rng: random.Random,
	config: GenerationConfig,
) -> tuple[list[dict], dict[str, int]]:
	restaurant_rows: list[dict] = []
	open_times: dict[str, int] = {}

	for idx in range(1, config.restaurant_count + 1):
		name = f"R{idx}"
		open_time = 0
		open_times[name] = open_time

		for table_size, (min_tables, max_tables) in TABLE_SIZE_DEFS:
			restaurant_rows.append(
				{
					"name": name,
					"strategy": config.strategy,
					"open_time": open_time,
					"table_size": table_size,
					"table_number": rng.randint(min_tables, max_tables),
				}
			)

	return restaurant_rows, open_times


def _generate_group_size(rng: random.Random, probabilities: tuple[float, float, float]) -> int:
	group_type = rng.choices(("A", "B", "C"), weights=probabilities, k=1)[0]
	if group_type == "A":
		return rng.randint(1, 2)
	if group_type == "B":
		return rng.randint(3, 4)
	return rng.randint(5, 6)


def _generate_customers(
	rng: random.Random,
	config: GenerationConfig,
	open_times: dict[str, int],
) -> list[dict]:
	customer_rows: list[dict] = []

	for restaurant_name in sorted(open_times.keys()):
		open_time = open_times[restaurant_name]
		current_time = open_time
		for index in range(1, config.customers_per_restaurant + 1):
			current_time += rng.choice(config.arrival_gaps)
			customer_rows.append(
				{
					"index": index,
					"restaurant": restaurant_name,
					"vip": 1 if rng.random() < config.vip_probability else 0,
					"number": _generate_group_size(rng, config.group_probabilities),
					"arrival_time": current_time,
				}
			)

	return customer_rows


def generate_dataset(config: GenerationConfig, seed: int, output_dir: Path) -> tuple[Path, Path]:
	rng = random.Random(seed)

	restaurant_rows, open_times = _generate_restaurants(rng, config)
	customer_rows = _generate_customers(rng, config, open_times)

	file_stem = (
		f"{config.strategy_label}_{config.restaurant_count}r_"
		f"{config.customers_per_restaurant}c_{config.arrival_gap_mode}"
	)
	restaurant_path = output_dir / f"testdata_restaurant_{file_stem}.csv"
	customer_path = output_dir / f"testdata_customer_{file_stem}.csv"

	_write_csv(
		restaurant_path,
		restaurant_rows,
		["name", "strategy", "open_time", "table_size", "table_number"],
	)
	_write_csv(
		customer_path,
		customer_rows,
		["index", "restaurant", "vip", "number", "arrival_time"],
	)

	return restaurant_path, customer_path


def build_parser() -> argparse.ArgumentParser:
	parser = argparse.ArgumentParser(
		description="Generate random restaurant/customer CSV data from interactive choices.",
	)
	parser.add_argument(
		"--seed",
		type=int,
		default=20260412,
		help="Base random seed. Different seeds generate different data.",
	)
	parser.add_argument(
		"--output-dir",
		type=Path,
		default=Path(__file__).resolve().parent / "simulated-data",
		help="Directory to place generated CSV files.",
	)
	return parser


def main() -> None:
	parser = build_parser()
	args = parser.parse_args()

	config = collect_config()
	print(f"Output directory: {args.output_dir}")
	restaurant_file, customer_file = generate_dataset(
		config=config,
		seed=args.seed,
		output_dir=args.output_dir,
	)
	print(f"Strategy: {config.strategy}")
	print(f"Restaurants: {config.restaurant_count}")
	print(f"Customers per restaurant: {config.customers_per_restaurant}")
	print(f"VIP probability: {config.vip_probability:.1%}")
	print(
		"Group probabilities: "
		f"A={config.group_probabilities[0]:.1%}, "
		f"B={config.group_probabilities[1]:.1%}, "
		f"C={config.group_probabilities[2]:.1%}"
	)
	print(f"Arrival interval mode: {config.arrival_gap_mode} {list(config.arrival_gaps)}")
	print(f"restaurant -> {restaurant_file}")
	print(f"customer   -> {customer_file}")


if __name__ == "__main__":
	main()
