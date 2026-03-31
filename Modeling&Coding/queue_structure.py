import heapq
from collections import deque


class State:
	"""State container for table occupancy and waiting queues."""

	def __init__(self, models=("A", "B", "C")):
		self.models = tuple(models)

		# Min-heap item: (leave_time, arrive_time, occupied_seats, customer_id)
		self.occupied = {model: [] for model in self.models}

		# Queue item: (arrive_time, customer_size, customer_id, wait_time)
		self.vip_queue = {model: deque() for model in self.models}
		self.non_vip_queue = {model: deque() for model in self.models}

	def _validate_model(self, model):
		if model not in self.models:
			raise ValueError(f"Unknown model '{model}'. Expected one of {self.models}.")

	def _select_queue(self, model, is_vip):
		self._validate_model(model)
		return self.vip_queue[model] if is_vip else self.non_vip_queue[model]

	# -----------------------------
	# Occupied min-heap operations
	# -----------------------------
	def push_occupied(self, model, leave_time, arrive_time, occupied_seats, customer_id):
		self._validate_model(model)
		heapq.heappush(
			self.occupied[model],
			(leave_time, arrive_time, occupied_seats, customer_id),
		)

	def pop_occupied(self, model):
		self._validate_model(model)
		if not self.occupied[model]:
			return None
		return heapq.heappop(self.occupied[model])

	def peek_occupied(self, model):
		self._validate_model(model)
		if not self.occupied[model]:
			return None
		return self.occupied[model][0]

	def occupied_size(self, model):
		self._validate_model(model)
		return len(self.occupied[model])

	# -----------------------------
	# Waiting queue operations
	# -----------------------------
	def enqueue_waiting(
		self,
		model,
		is_vip,
		arrive_time,
		customer_size,
		customer_id,
		wait_time=0,
		dinning_time=30
	):
		q = self._select_queue(model, is_vip)
		q.append((arrive_time, customer_size, customer_id, wait_time, dinning_time))

	def dequeue_waiting(self, model, is_vip):
		q = self._select_queue(model, is_vip)
		if not q:
			return None
		return q.popleft()

	def peek_waiting(self, model, is_vip):
		q = self._select_queue(model, is_vip)
		if not q:
			return None
		return q[0]

	def waiting_size(self, model, is_vip):
		q = self._select_queue(model, is_vip)
		return len(q)

	# -----------------------------
	# Utility operations
	# -----------------------------
	def clear_model(self, model):
		self._validate_model(model)
		self.occupied[model].clear()
		self.vip_queue[model].clear()
		self.non_vip_queue[model].clear()

	def clear_all(self):
		for model in self.models:
			self.clear_model(model)

	def show(self):
		"""Return a snapshot of all queues/heaps in plain Python containers."""
		return {
			"occupied": {
				model: sorted(self.occupied[model]) for model in self.models
			},
			"vip_queue": {
				model: list(self.vip_queue[model]) for model in self.models
			},
			"non_vip_queue": {
				model: list(self.non_vip_queue[model]) for model in self.models
			},
		}

	def is_model_empty(self, model):
		self._validate_model(model)

		occupied_empty = not self.occupied[model]
		vip_empty = not self.vip_queue[model]
		non_vip_empty = not self.non_vip_queue[model]

		return occupied_empty and vip_empty and non_vip_empty

	def is_empty(self):
		return all(self.is_model_empty(model) for model in self.models)
