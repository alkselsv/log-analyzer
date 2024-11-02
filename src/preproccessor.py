"""Определение класса Preprocessor"""
import os
from datetime import datetime
import warnings
import numpy as np
import pandas as pd
import json
from logging import Logger

warnings.filterwarnings("ignore")


class Preprocessor:
    """Предобработчик данных"""

    def __init__(self, logger: Logger | None = None) -> None:
        self.logger: Logger | None = logger
        self.last_file_positions: dict[str, int] = {}
        self.last_file_sizes: dict[str, int] = {}

    @staticmethod
    def get_min(lst: list[float]) -> float:
        arr = np.array(lst, dtype=np.float32)
        return np.nanmin(arr) if arr.size > 0 else 0

    @staticmethod
    def get_max(lst: list[float]) -> float:
        arr = np.array(lst, dtype=np.float32)
        return np.nanmax(arr) if arr.size > 0 else 0

    @staticmethod
    def get_mean(lst: list[float]) -> float:
        arr = np.array(lst, dtype=np.float32)
        return np.nanmean(arr) if arr.size > 0 else 0

    def preproccess_session(
        self, session_id: str, site_session: list[dict[str, any]]
    ) -> dict[str, any]:
        res: dict[str, any] = {}
        res["session_id"] = session_id
        uas: list[str] = []
        ips: list[str] = []
        timestamps: list[int] = []

        mousemove_prm_data_b_n = []
        mousemove_prm_data_b_ms = []
        mousemove_prm_data_b_l = []
        mousemove_prm_data_b_cxy2 = []

        mousemove_prm_data_td_sm = []
        mousemove_prm_data_td_mn = []
        mousemove_prm_data_td_mx = []
        mousemove_prm_data_td_gr = []

        mousemove_prm_data_x_sm = []
        mousemove_prm_data_x_mn = []
        mousemove_prm_data_x_mx = []
        mousemove_prm_data_x_gr = []

        mousemove_prm_data_y_sm = []
        mousemove_prm_data_y_mn = []
        mousemove_prm_data_y_mx = []
        mousemove_prm_data_y_gr = []

        mousemove_prm_data_s_sm = []
        mousemove_prm_data_s_mn = []
        mousemove_prm_data_s_mx = []
        mousemove_prm_data_s_gr = []

        mousemove_prm_data_v_sm = []
        mousemove_prm_data_v_mn = []
        mousemove_prm_data_v_mx = []
        mousemove_prm_data_v_gr = []

        mousemove_prm_data_a_sm = []
        mousemove_prm_data_a_mn = []
        mousemove_prm_data_a_mx = []
        mousemove_prm_data_a_gr = []

        mousemove_prm_data_u_sm = []
        mousemove_prm_data_u_mn = []
        mousemove_prm_data_u_mx = []
        mousemove_prm_data_u_gr = []

        mousemove_prm_data_ud_sm = []
        mousemove_prm_data_ud_mn = []
        mousemove_prm_data_ud_mx = []
        mousemove_prm_data_ud_gr = []

        mousemove_prm_data_u2_sm = []
        mousemove_prm_data_u2_mn = []
        mousemove_prm_data_u2_mx = []
        mousemove_prm_data_u2_gr = []

        for record in site_session:
            if record["type"] == "CLIENT":
                uas.append(record["ua"]["v"])

            if record["type"] == "METRIK":
                if record["act"] == "move":
                    ips.append(record["ip"])
                    timestamps.append(record["ts"])

                    mousemove_prm_data = record["prm"]["data"]

                    if mousemove_prm_data["_b"]:
                        mousemove_prm_data_b_ms.append(mousemove_prm_data["_b"]["n"])
                        mousemove_prm_data_b_ms.append(mousemove_prm_data["_b"]["ms"])
                        mousemove_prm_data_b_l.append(mousemove_prm_data["_b"]["l"])

                    if mousemove_prm_data["td"]:
                        mousemove_prm_data_td_sm.append(mousemove_prm_data["td"]["sm"])
                        mousemove_prm_data_td_mn.append(
                            mousemove_prm_data["td"]["mn"][0]
                        )
                        mousemove_prm_data_td_mx.append(
                            mousemove_prm_data["td"]["mx"][0]
                        )
                        mousemove_prm_data_td_gr.append(
                            mousemove_prm_data["td"]["gr"][0]
                        )

                    if mousemove_prm_data["x"]:
                        mousemove_prm_data_x_sm.append(mousemove_prm_data["x"]["sm"])
                        mousemove_prm_data_x_mn.append(mousemove_prm_data["x"]["mn"][0])
                        mousemove_prm_data_x_mx.append(mousemove_prm_data["x"]["mx"][0])
                        mousemove_prm_data_x_gr.append(mousemove_prm_data["x"]["gr"][0])

                    if mousemove_prm_data["y"]:
                        mousemove_prm_data_y_sm.append(mousemove_prm_data["y"]["sm"])
                        mousemove_prm_data_y_mn.append(mousemove_prm_data["y"]["mn"][0])
                        mousemove_prm_data_y_mx.append(mousemove_prm_data["y"]["mx"][0])
                        mousemove_prm_data_y_gr.append(mousemove_prm_data["y"]["gr"][0])

                    if mousemove_prm_data["s"]:
                        mousemove_prm_data_s_sm.append(mousemove_prm_data["s"]["sm"])
                        mousemove_prm_data_s_mn.append(mousemove_prm_data["s"]["mn"][0])
                        mousemove_prm_data_s_mx.append(mousemove_prm_data["s"]["mx"][0])
                        mousemove_prm_data_s_gr.append(mousemove_prm_data["s"]["gr"][0])

                    if mousemove_prm_data["v"]:
                        mousemove_prm_data_v_sm.append(mousemove_prm_data["v"]["sm"])
                        mousemove_prm_data_v_mn.append(mousemove_prm_data["v"]["mn"][0])
                        mousemove_prm_data_v_mx.append(mousemove_prm_data["v"]["mx"][0])
                        mousemove_prm_data_v_gr.append(mousemove_prm_data["v"]["gr"][0])

                    if mousemove_prm_data["a"]:
                        mousemove_prm_data_a_sm.append(mousemove_prm_data["a"]["sm"])
                        mousemove_prm_data_a_mn.append(mousemove_prm_data["a"]["mn"][0])
                        mousemove_prm_data_a_mx.append(mousemove_prm_data["a"]["mx"][0])
                        mousemove_prm_data_a_gr.append(mousemove_prm_data["a"]["gr"][0])

                    if mousemove_prm_data["u"]:
                        mousemove_prm_data_u_sm.append(mousemove_prm_data["u"]["sm"])
                        mousemove_prm_data_u_mn.append(mousemove_prm_data["u"]["mn"][0])
                        mousemove_prm_data_u_mx.append(mousemove_prm_data["u"]["mx"][0])
                        mousemove_prm_data_u_gr.append(mousemove_prm_data["u"]["gr"][0])

                    if mousemove_prm_data["ud"]:
                        mousemove_prm_data_ud_sm.append(mousemove_prm_data["ud"]["sm"])
                        mousemove_prm_data_ud_mn.append(
                            mousemove_prm_data["ud"]["mn"][0]
                        )
                        mousemove_prm_data_ud_mx.append(
                            mousemove_prm_data["ud"]["mx"][0]
                        )
                        mousemove_prm_data_ud_gr.append(
                            mousemove_prm_data["ud"]["gr"][0]
                        )

                    if mousemove_prm_data["u2"]:
                        mousemove_prm_data_u2_sm.append(mousemove_prm_data["u2"]["sm"])
                        mousemove_prm_data_u2_mn.append(
                            mousemove_prm_data["u2"]["mn"][0]
                        )
                        mousemove_prm_data_u2_mx.append(
                            mousemove_prm_data["u2"]["mx"][0]
                        )
                        mousemove_prm_data_u2_gr.append(
                            mousemove_prm_data["u2"]["gr"][0]
                        )

        res["ua"] = uas[0]
        res["ip"] = ips[0]
        res["timestamp"] = timestamps[0]

        # mousemove_prm_data_b_ms
        res["mousemove_prm_data_b_ms_min"] = self.get_min(mousemove_prm_data_b_ms)
        res["mousemove_prm_data_b_ms_max"] = self.get_max(mousemove_prm_data_b_ms)
        res["mousemove_prm_data_b_ms_mean"] = self.get_mean(mousemove_prm_data_b_ms)

        # mousemove_prm_data_b_l
        res["mousemove_prm_data_b_l_min"] = self.get_min(mousemove_prm_data_b_l)
        res["mousemove_prm_data_a_l_max"] = self.get_max(mousemove_prm_data_b_l)
        res["mousemove_prm_data_a_l_mean"] = self.get_mean(mousemove_prm_data_b_l)

        # mousemove_prm_data_b_n
        res["mousemove_prm_data_b_n_min"] = self.get_min(mousemove_prm_data_b_n)
        res["mousemove_prm_data_a_n_max"] = self.get_max(mousemove_prm_data_b_n)
        res["mousemove_prm_data_a_n_mean"] = self.get_mean(mousemove_prm_data_b_n)

        # mousemove_prm_data_td
        res["mousemove_prm_data_td_sm_min"] = self.get_min(mousemove_prm_data_td_sm)
        res["mousemove_prm_data_td_mn_min"] = self.get_min(mousemove_prm_data_td_mn)
        res["mousemove_prm_data_td_mx_min"] = self.get_min(mousemove_prm_data_td_mx)
        res["mousemove_prm_data_td_gr_min"] = self.get_min(mousemove_prm_data_td_gr)

        res["mousemove_prm_data_td_sm_max"] = self.get_max(mousemove_prm_data_td_sm)
        res["mousemove_prm_data_td_mn_max"] = self.get_max(mousemove_prm_data_td_mn)
        res["mousemove_prm_data_td_mx_max"] = self.get_max(mousemove_prm_data_td_mx)
        res["mousemove_prm_data_td_gr_max"] = self.get_max(mousemove_prm_data_td_gr)

        res["mousemove_prm_data_td_sm_mean"] = self.get_mean(mousemove_prm_data_td_sm)
        res["mousemove_prm_data_td_mn_mean"] = self.get_mean(mousemove_prm_data_td_mn)
        res["mousemove_prm_data_td_mx_mean"] = self.get_mean(mousemove_prm_data_td_mx)
        res["mousemove_prm_data_td_gr_mean"] = self.get_mean(mousemove_prm_data_td_gr)

        # mousemove_prm_data_x
        res["mousemove_prm_data_x_sm_min"] = self.get_min(mousemove_prm_data_x_sm)
        res["mousemove_prm_data_x_mn_min"] = self.get_min(mousemove_prm_data_x_mn)
        res["mousemove_prm_data_x_mx_min"] = self.get_min(mousemove_prm_data_x_mx)
        res["mousemove_prm_data_x_gr_min"] = self.get_min(mousemove_prm_data_x_gr)

        res["mousemove_prm_data_x_sm_max"] = self.get_max(mousemove_prm_data_x_sm)
        res["mousemove_prm_data_x_mn_max"] = self.get_max(mousemove_prm_data_x_mn)
        res["mousemove_prm_data_x_mx_max"] = self.get_max(mousemove_prm_data_x_mx)
        res["mousemove_prm_data_x_gr_max"] = self.get_max(mousemove_prm_data_x_gr)

        res["mousemove_prm_data_x_sm_mean"] = self.get_mean(mousemove_prm_data_x_sm)
        res["mousemove_prm_data_x_mn_mean"] = self.get_mean(mousemove_prm_data_x_mn)
        res["mousemove_prm_data_x_mx_mean"] = self.get_mean(mousemove_prm_data_x_mx)
        res["mousemove_prm_data_x_gr_mean"] = self.get_mean(mousemove_prm_data_x_gr)

        # mousemove_prm_data_y
        res["mousemove_prm_data_y_sm_min"] = self.get_min(mousemove_prm_data_y_sm)
        res["mousemove_prm_data_y_mn_min"] = self.get_min(mousemove_prm_data_y_mn)
        res["mousemove_prm_data_y_mx_min"] = self.get_min(mousemove_prm_data_y_mx)
        res["mousemove_prm_data_y_gr_min"] = self.get_min(mousemove_prm_data_y_gr)

        res["mousemove_prm_data_y_sm_max"] = self.get_max(mousemove_prm_data_y_sm)
        res["mousemove_prm_data_y_mn_max"] = self.get_max(mousemove_prm_data_y_mn)
        res["mousemove_prm_data_y_mx_max"] = self.get_max(mousemove_prm_data_y_mx)
        res["mousemove_prm_data_y_gr_max"] = self.get_max(mousemove_prm_data_y_gr)

        res["mousemove_prm_data_y_sm_mean"] = self.get_mean(mousemove_prm_data_y_sm)
        res["mousemove_prm_data_y_mn_mean"] = self.get_mean(mousemove_prm_data_y_mn)
        res["mousemove_prm_data_y_mx_mean"] = self.get_mean(mousemove_prm_data_y_mx)
        res["mousemove_prm_data_y_gr_mean"] = self.get_mean(mousemove_prm_data_y_gr)

        # mousemove_prm_data_s
        res["mousemove_prm_data_s_sm_min"] = self.get_min(mousemove_prm_data_s_sm)
        res["mousemove_prm_data_s_mn_min"] = self.get_min(mousemove_prm_data_s_mn)
        res["mousemove_prm_data_s_mx_min"] = self.get_min(mousemove_prm_data_s_mx)
        res["mousemove_prm_data_s_gr_min"] = self.get_min(mousemove_prm_data_s_gr)

        res["mousemove_prm_data_s_sm_max"] = self.get_max(mousemove_prm_data_s_sm)
        res["mousemove_prm_data_s_mn_max"] = self.get_max(mousemove_prm_data_s_mn)
        res["mousemove_prm_data_s_mx_max"] = self.get_max(mousemove_prm_data_s_mx)
        res["mousemove_prm_data_s_gr_max"] = self.get_max(mousemove_prm_data_s_gr)

        res["mousemove_prm_data_s_sm_mean"] = self.get_mean(mousemove_prm_data_s_sm)
        res["mousemove_prm_data_s_mn_mean"] = self.get_mean(mousemove_prm_data_s_mn)
        res["mousemove_prm_data_s_mx_mean"] = self.get_mean(mousemove_prm_data_s_mx)
        res["mousemove_prm_data_s_gr_mean"] = self.get_mean(mousemove_prm_data_s_gr)

        # mousemove_prm_data_v
        res["mousemove_prm_data_v_sm_min"] = self.get_min(mousemove_prm_data_v_sm)
        res["mousemove_prm_data_v_mn_min"] = self.get_min(mousemove_prm_data_v_mn)
        res["mousemove_prm_data_v_mx_min"] = self.get_min(mousemove_prm_data_v_mx)
        res["mousemove_prm_data_v_gr_min"] = self.get_min(mousemove_prm_data_v_gr)

        res["mousemove_prm_data_v_sm_max"] = self.get_max(mousemove_prm_data_v_sm)
        res["mousemove_prm_data_v_mn_max"] = self.get_max(mousemove_prm_data_v_mn)
        res["mousemove_prm_data_v_mx_max"] = self.get_max(mousemove_prm_data_v_mx)
        res["mousemove_prm_data_v_gr_max"] = self.get_max(mousemove_prm_data_v_gr)

        res["mousemove_prm_data_v_sm_mean"] = self.get_mean(mousemove_prm_data_v_sm)
        res["mousemove_prm_data_v_mn_mean"] = self.get_mean(mousemove_prm_data_v_mn)
        res["mousemove_prm_data_v_mx_mean"] = self.get_mean(mousemove_prm_data_v_mx)
        res["mousemove_prm_data_v_gr_mean"] = self.get_mean(mousemove_prm_data_v_gr)

        # mousemove_prm_data_a
        res["mousemove_prm_data_a_sm_min"] = self.get_min(mousemove_prm_data_a_sm)
        res["mousemove_prm_data_a_mn_min"] = self.get_min(mousemove_prm_data_a_mn)
        res["mousemove_prm_data_a_mx_min"] = self.get_min(mousemove_prm_data_a_mx)
        res["mousemove_prm_data_a_gr_min"] = self.get_min(mousemove_prm_data_a_gr)

        res["mousemove_prm_data_a_sm_max"] = self.get_max(mousemove_prm_data_a_sm)
        res["mousemove_prm_data_a_mn_max"] = self.get_max(mousemove_prm_data_a_mn)
        res["mousemove_prm_data_a_mx_max"] = self.get_max(mousemove_prm_data_a_mx)
        res["mousemove_prm_data_a_gr_max"] = self.get_max(mousemove_prm_data_a_gr)

        res["mousemove_prm_data_a_sm_mean"] = self.get_mean(mousemove_prm_data_a_sm)
        res["mousemove_prm_data_a_mn_mean"] = self.get_mean(mousemove_prm_data_a_mn)
        res["mousemove_prm_data_a_mx_mean"] = self.get_mean(mousemove_prm_data_a_mx)
        res["mousemove_prm_data_a_gr_mean"] = self.get_mean(mousemove_prm_data_a_gr)

        # mousemove_prm_data_u
        res["mousemove_prm_data_u_sm_min"] = self.get_min(mousemove_prm_data_u_sm)
        res["mousemove_prm_data_u_mn_min"] = self.get_min(mousemove_prm_data_u_mn)
        res["mousemove_prm_data_u_mx_min"] = self.get_min(mousemove_prm_data_u_mx)
        res["mousemove_prm_data_u_gr_min"] = self.get_min(mousemove_prm_data_u_gr)

        res["mousemove_prm_data_u_sm_max"] = self.get_max(mousemove_prm_data_u_sm)
        res["mousemove_prm_data_u_mn_max"] = self.get_max(mousemove_prm_data_u_mn)
        res["mousemove_prm_data_u_mx_max"] = self.get_max(mousemove_prm_data_u_mx)
        res["mousemove_prm_data_u_gr_max"] = self.get_max(mousemove_prm_data_u_gr)

        res["mousemove_prm_data_u_sm_mean"] = self.get_mean(mousemove_prm_data_u_sm)
        res["mousemove_prm_data_u_mn_mean"] = self.get_mean(mousemove_prm_data_u_mn)
        res["mousemove_prm_data_u_mx_mean"] = self.get_mean(mousemove_prm_data_u_mx)
        res["mousemove_prm_data_u_gr_mean"] = self.get_mean(mousemove_prm_data_u_gr)

        # mousemove_prm_data_ud
        res["mousemove_prm_data_ud_sm_min"] = self.get_min(mousemove_prm_data_ud_sm)
        res["mousemove_prm_data_ud_mn_min"] = self.get_min(mousemove_prm_data_ud_mn)
        res["mousemove_prm_data_ud_mx_min"] = self.get_min(mousemove_prm_data_ud_mx)
        res["mousemove_prm_data_ud_gr_min"] = self.get_min(mousemove_prm_data_ud_gr)

        res["mousemove_prm_data_ud_sm_max"] = self.get_max(mousemove_prm_data_ud_sm)
        res["mousemove_prm_data_ud_mn_max"] = self.get_max(mousemove_prm_data_ud_mn)
        res["mousemove_prm_data_ud_mx_max"] = self.get_max(mousemove_prm_data_ud_mx)
        res["mousemove_prm_data_ud_gr_max"] = self.get_max(mousemove_prm_data_ud_gr)

        res["mousemove_prm_data_ud_sm_mean"] = self.get_mean(mousemove_prm_data_ud_sm)
        res["mousemove_prm_data_ud_mn_mean"] = self.get_mean(mousemove_prm_data_ud_mn)
        res["mousemove_prm_data_ud_mx_mean"] = self.get_mean(mousemove_prm_data_ud_mx)
        res["mousemove_prm_data_ud_gr_mean"] = self.get_mean(mousemove_prm_data_ud_gr)

        # mousemove_prm_data_u2
        res["mousemove_prm_data_u2_sm_min"] = self.get_min(mousemove_prm_data_u2_sm)
        res["mousemove_prm_data_u2_mn_min"] = self.get_min(mousemove_prm_data_u2_mn)
        res["mousemove_prm_data_u2_mx_min"] = self.get_min(mousemove_prm_data_u2_mx)
        res["mousemove_prm_data_u2_gr_min"] = self.get_min(mousemove_prm_data_u2_gr)

        res["mousemove_prm_data_u2_sm_max"] = self.get_max(mousemove_prm_data_u2_sm)
        res["mousemove_prm_data_u2_mn_max"] = self.get_max(mousemove_prm_data_u2_mn)
        res["mousemove_prm_data_u2_mx_max"] = self.get_max(mousemove_prm_data_u2_mx)
        res["mousemove_prm_data_u2_gr_max"] = self.get_max(mousemove_prm_data_u2_gr)

        res["mousemove_prm_data_u2_sm_mean"] = self.get_mean(mousemove_prm_data_u2_sm)
        res["mousemove_prm_data_u2_mn_mean"] = self.get_mean(mousemove_prm_data_u2_mn)
        res["mousemove_prm_data_u2_mx_mean"] = self.get_mean(mousemove_prm_data_u2_mx)
        res["mousemove_prm_data_u2_gr_mean"] = self.get_mean(mousemove_prm_data_u2_gr)

        return res

    def _read_data(self, file: str) -> dict[str, list[dict[str, any]]]:
        """Загружает данные в словарь сессий"""
        merged_data_by_sess_ab: dict[str, list[dict[str, any]]] = {}

        with open(file, "r") as f:
            current_file_size = os.path.getsize(file)
            last_file_position = self.last_file_positions.get(file, 0)
            if current_file_size < self.last_file_sizes.get(file, 0):
                last_file_position = 0
                self.last_file_positions[file] = 0
            self.last_file_sizes[file] = current_file_size
            f.seek(last_file_position)
            for line in f:
                record = json.loads(line)
                key_a = record["sess"]["a"]
                key_b = record["sess"]["b"]
                key = key_a + "." + key_b
                if key not in merged_data_by_sess_ab:
                    merged_data_by_sess_ab[key] = []
                merged_data_by_sess_ab[key].append(record)
            self.last_file_positions[file] = f.tell()

        return merged_data_by_sess_ab

    def _preproccess_data(
        self, sessions: dict[str, list[dict[str, any]]]
    ) -> list[dict[str, any]]:
        """Выполняет предобаботку данных"""

        # Очистка от коротких сессий
        records_in_sessions = {}
        session_ids = list((sessions.keys()))

        for session_id in session_ids:
            records_in_sessions[session_id] = len(sessions[session_id])

        session_ids_cleaned_iter1 = []

        for session_id in session_ids:
            if records_in_sessions[session_id] > 1:
                session_ids_cleaned_iter1.append(session_id)

        # Очистка от сессий, в которых нет move
        session_ids_cleaned_iter2 = []

        for session_id in session_ids_cleaned_iter1:
            for record in sessions[session_id]:
                if record["type"] == "METRIK":
                    if record["act"] == "move":
                        session_ids_cleaned_iter2.append(session_id)
                        break

        session_ids_cleaned = session_ids_cleaned_iter2
        keys = session_ids_cleaned

        dataset = []

        for key in keys:
            site_session = sessions[key]
            res = self.preproccess_session(key, site_session)
            if res:
                dataset.append(res)

        return dataset

    def _postproccess_data(
        self, data: list[dict[str, any]]
    ) -> tuple[list[str], list[str], list[int], pd.DataFrame]:
        """Выполняет создание новых признаков"""
        df = pd.DataFrame.from_dict(data)
        df.fillna(0, inplace=True)
      
        sessions = df.get(df.columns[0])
        uas = df.get(df.columns[1])
        ips = df.get(df.columns[2])
        timestamps = df.get(df.columns[3])
        dataframe = df.get(df.columns[4:])
        return sessions, uas, ips, timestamps, dataframe

    def proccess_data(
        self, file: str
    ) -> tuple[list[str], list[str], list[int], pd.DataFrame]:
        """Запускает процесс обработки данных"""

        sessions = self._read_data(file)
        if sessions:
            self.logger.info("Sessions loaded")
            dataset = self._preproccess_data(sessions)
            self.logger.info("Sessions preproccessed")

            if dataset:
                (sessions, uas, ips, timestamps, dataset) = self._postproccess_data(dataset)
                self.logger.info("Sessions postproccessed")
            else:
                sessions, uas, ips, timestamps, dataset = [], [], [], [], []
                self.logger.info("No sessions")
        else:
            sessions, uas, ips, timestamps, dataset = [], [], [], [], []
        return sessions, uas, ips, timestamps, dataset

