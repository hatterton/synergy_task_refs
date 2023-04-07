from collections import defaultdict
from typing import (
    List,
    Dict,
    Tuple,
    Iterable,
)
import json

from refs.entities import (
    User,
    RefLevel,
    UserGraph,
)


Depth = int
IsPodUser = User  # child of user
UserStackPos = Tuple[User, IsPodUser, Depth]
UserStack = List[UserStackPos]
RefStack = Dict[RefLevel, UserStack]


class UserGraphLoader:
    def __init__(self) -> None:
        self._direct_payments = {
            RefLevel.V1: 30,
            RefLevel.V2: 40,
            RefLevel.V3: 50,
            RefLevel.V4: 60,
            RefLevel.V5: 65,
            RefLevel.V6: 70,
        }

        self._ref_payments = {
            (RefLevel.V1, RefLevel.V2): 10,

            (RefLevel.V1, RefLevel.V3): 20,
            (RefLevel.V2, RefLevel.V3): 10,

            (RefLevel.V1, RefLevel.V4): 30,
            (RefLevel.V2, RefLevel.V4): 20,
            (RefLevel.V3, RefLevel.V4): 10,

            (RefLevel.V1, RefLevel.V5): 35,
            (RefLevel.V2, RefLevel.V5): 25,
            (RefLevel.V3, RefLevel.V5): 15,
            (RefLevel.V4, RefLevel.V5): 5,

            (RefLevel.V1, RefLevel.V6): 40,
            (RefLevel.V2, RefLevel.V6): 30,
            (RefLevel.V3, RefLevel.V6): 20,
            (RefLevel.V4, RefLevel.V6): 10,
            (RefLevel.V5, RefLevel.V6): 5,
        }

    def load(self, data_path: str) -> UserGraph:
        with open(data_path, "r") as f:
            dict_data = json.load(f)

        user_graph = self._convert_dict2user_graph(dict_data)
        self._evaluate_ref_level(user_graph)
        self._evaluate_payments(user_graph)

        return user_graph

    def _convert_dict2user_graph(self, dict_data: dict) -> UserGraph:
        root = self._build_user(dict_data)

        return UserGraph(root=root)

    def _build_user(self, dict_data: dict) -> User:
        user = User(pk=dict_data["id"])

        for subdict_data in dict_data["refs"]:
            user.refs.append(self._build_user(subdict_data))

        return user

    def _evaluate_ref_level(self, user_graph: UserGraph) -> None:
        self._evaluate_user_ref_level(user_graph.root)

    def _evaluate_user_ref_level(self, user: User) -> None:
        for ref_user in user.refs:
            self._evaluate_user_ref_level(ref_user)

        user.team_size = sum([ref.team_size + 1 for ref in user.refs])
        user.ref_level = self._get_ref_level(user)

    def _get_ref_level(self, user: User) -> RefLevel:
        level_and_checkers = [
            (RefLevel.V6, self._is_v6_ref_level),
            (RefLevel.V5, self._is_v5_ref_level),
            (RefLevel.V4, self._is_v4_ref_level),
            (RefLevel.V3, self._is_v3_ref_level),
            (RefLevel.V2, self._is_v2_ref_level),
        ]

        for level, checker in level_and_checkers:
            if checker(user):
                return level

        return RefLevel.V1

    def _is_v2_ref_level(self, user: User) -> bool:
        return user.team_size >= 20 and len(user.refs) >= 3

    def _is_v3_ref_level(self, user: User) -> bool:
        v2_refs = [r for r in user.refs if r.ref_level == RefLevel.V2]
        return user.team_size >= 100 and len(user.refs) >= 5 and len(v2_refs) >= 3

    def _is_v4_ref_level(self, user: User) -> bool:
        v3_refs = [r for r in user.refs if r.ref_level == RefLevel.V3]
        return user.team_size >= 300 and len(user.refs) >= 8 and len(v3_refs) >= 3

    def _is_v5_ref_level(self, user: User) -> bool:
        v4_refs = [r for r in user.refs if r.ref_level == RefLevel.V4]
        return user.team_size >= 800 and len(user.refs) >= 12 and len(v4_refs) >= 3

    def _is_v6_ref_level(self, user: User) -> bool:
        v5_refs = [r for r in user.refs if r.ref_level == RefLevel.V5]
        return user.team_size >= 1500 and len(user.refs) >= 20 and len(v5_refs) >= 3


    def _evaluate_payments(self, user_graph: UserGraph) -> None:
        user_stack: RefStack = defaultdict(list)

        self._evaluate_user_payments(
            user=user_graph.root,
            depth=0,
            ref_stack=user_stack,
        )

    def _evaluate_user_payments(self, user: User, depth: int, ref_stack: RefStack) -> None:
        for ref in user.refs:
            self._apply_transfer(ref, user, self._direct_payments[user.ref_level])

        ref_levels = [RefLevel.V6, RefLevel.V5, RefLevel.V4, RefLevel.V3, RefLevel.V2]
        for ref in user.refs:
            last_depth = 0
            for ref_level in ref_levels:
                if ref.ref_level.value >= ref_level.value:
                    continue

                user_stack = ref_stack[ref_level]
                if not user_stack:
                    continue

                parent, is_pod_user, parent_depth = user_stack[-1]
                if last_depth > parent_depth:
                    continue

                amount_key = (is_pod_user.ref_level, parent.ref_level)
                if amount_key in self._ref_payments:
                    amount = self._ref_payments[amount_key]
                    self._apply_transfer(ref, parent, amount)

                    last_depth = parent_depth

        for ref in user.refs:
            ref_stack[user.ref_level].append((user, ref, depth))

            self._evaluate_user_payments(ref, depth+1, ref_stack)

            ref_stack[user.ref_level].pop()

    def _apply_transfer(self, source: User, target: User, amount: int) -> None:
        source.balance -= amount
        target.balance += amount


