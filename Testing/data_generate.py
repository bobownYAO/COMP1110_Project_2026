from __future__ import annotations

import argparse
import csv
import random
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ScaleConfig:
	min_restaurants: int
	max_restaurants: int
	min_customers_per_restaurant: int
	max_customers_per_restaurant: int
	min_open_time: int
	max_open_time: int


SCALE_CONFIGS: dict[str, ScaleConfig] = {
	"small": ScaleConfig(
		min_restaurants=2,
		max_restaurants=5,
		min_customers_per_restaurant=20,
		max_customers_per_restaurant=100,
		min_open_time=0,
		max_open_time=20,
	),
	"medium": ScaleConfig(
		min_restaurants=5,
		max_restaurants=20,
		min_customers_per_restaurant=40,
		max_customers_per_restaurant=200,
		min_open_time=0,
		max_open_time=40,
	),
	"large": ScaleConfig(
		min_restaurants=20,
		max_restaurants=100,
		min_customers_per_restaurant=80,
		max_customers_per_restaurant=300,
		min_open_time=0,
		max_open_time=60,
	),
}


TABLE_SIZE_DEFS = [
	("A", (2, 8)),
	("B", (1, 6)),
	("C", (1, 5)),
]
SUPPORTED_STRATEGIES = ["vip", "single_snake", "size_base"]


def _write_csv(file_path: Path, rows: list[dict], columns: list[str]) -> None:
	file_path.parent.mkdir(parents=True, exist_ok=True)
	with file_path.open("w", newline="", encoding="utf-8") as f:
		writer = csv.DictWriter(f, fieldnames=columns)
		writer.writeheader()
		writer.writerows(rows)


def _generate_restaurants(
	rng: random.Random,
	scale: ScaleConfig,
) -> tuple[list[dict], dict[str, int]]:
	restaurant_rows: list[dict] = []
	open_times: dict[str, int] = {}

	restaurant_count = rng.randint(scale.min_restaurants, scale.max_restaurants)
	for idx in range(1, restaurant_count + 1):
		name = f"R{idx}"
		strategy = rng.choice(SUPPORTED_STRATEGIES)
		open_time = rng.randint(scale.min_open_time, scale.max_open_time)
		open_times[name] = open_time

		for table_size, (min_tables, max_tables) in TABLE_SIZE_DEFS:
			restaurant_rows.append(
				{
					"name": name,
					"strategy": strategy,
					"open_time": open_time,
					"table_size": table_size,
					"table_number": rng.randint(min_tables, max_tables),
				}
			)

	return restaurant_rows, open_times


def _generate_customers(
	rng: random.Random,
	scale: ScaleConfig,
	open_times: dict[str, int],
) -> list[dict]:
	customer_rows: list[dict] = []

	for restaurant_name in sorted(open_times.keys()):
		open_time = open_times[restaurant_name]
		customer_count = rng.randint(
			scale.min_customers_per_restaurant,
			scale.max_customers_per_restaurant,
		)

		current_time = open_time
		for index in range(1, customer_count + 1):
			# Randomly keep same arrival time for burst arrivals.
			current_time += rng.choice([0, 0, 1, 1, 2, 3, 5, 7])
			customer_rows.append(
				{
					"index": index,
					"restaurant": restaurant_name,
					"vip": 1 if rng.random() < 0.2 else 0,
					"number": rng.randint(1, 10),
					"arrival_time": current_time,
				}
			)

	return customer_rows


def generate_one_scale(scale_name: str, seed: int, output_dir: Path) -> tuple[Path, Path]:
	if scale_name not in SCALE_CONFIGS:
		valid = ", ".join(SCALE_CONFIGS.keys())
		raise ValueError(f"Unknown scale '{scale_name}'. Valid values: {valid}")

	rng = random.Random(seed)
	config = SCALE_CONFIGS[scale_name]

	restaurant_rows, open_times = _generate_restaurants(rng, config)
	customer_rows = _generate_customers(rng, config, open_times)

	restaurant_path = output_dir / f"testdata_restaurant_{scale_name}.csv"
	customer_path = output_dir / f"testdata_customer_{scale_name}.csv"

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
		description="Generate random restaurant/customer CSV data for all scales.",
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

	print(f"Output directory: {args.output_dir}")
	for offset, scale_name in enumerate(["small", "medium", "large"]):
		restaurant_file, customer_file = generate_one_scale(
			scale_name=scale_name,
			seed=args.seed + offset,
			output_dir=args.output_dir,
		)
		print(f"[{scale_name}] restaurant -> {restaurant_file}")
		print(f"[{scale_name}] customer   -> {customer_file}")


if __name__ == "__main__":
	main()
