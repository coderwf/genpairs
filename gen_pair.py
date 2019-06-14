# -*- coding:utf-8 -*-

# 生成可以进行对比的文件
import pandas as pd
import random


class PairGen:
    DIFF = 0
    DROP = 1
    NEW = 2

    def __init__(self, rows_c, headers_c=99, file_name=None):
        if not file_name:
            self.origin, self.target = "origin.xlsx", "target.xlsx"
        else:
            self.origin, self.target = "origin_%s.xlsx" % file_name, "target_%s.xlsx" % file_name
        self.rows_c = rows_c
        self.emp_id_auto = 0
        self.headers_c = headers_c
        self.headers = self.get_headers()

    @property
    def emp_id_auto_incr(self):
        self.emp_id_auto += 1
        return self.emp_id_auto

    def get_headers(self):
        headers = ["工号"]
        for header_c in range(self.headers_c):
            headers.append("header_%s" % header_c)
        return headers

    def gen_row(self):
        row = [self.emp_id_auto_incr]
        for i in range(self.headers_c):
            row.append(random.randint(1, 100))
        return row

    @staticmethod
    def change_row(row):
        new_row = [row[0]]
        for item in row[1:]:
            if random.randint(0, 2) == 0:
                new_row.append(item+1)
            else:
                new_row.append(item)
        return new_row

    def gen_pair(self):
        origin_data = []
        target_data = []
        for row_c in range(self.rows_c):
            if row_c % 10000 == 0:
                print(row_c)
            row = self.gen_row()
            diff_type = random.randint(0, 50)
            if diff_type == self.DROP:
                origin_data.append(row)
            elif diff_type == self.NEW:
                target_data.append(row)
            else:
                origin_data.append(row)
                row = self.change_row(row)
                target_data.append(row)

        origin_df = pd.DataFrame(data=origin_data, columns=self.headers)
        target_df = pd.DataFrame(data=target_data, columns=self.headers)

        origin_df.set_index(self.headers[0], inplace=True)
        target_df.set_index(self.headers[0], inplace=True)

        origin_writer = pd.ExcelWriter(self.origin, engine="xlsxwriter")
        target_writer = pd.ExcelWriter(self.target, engine="xlsxwriter")
        origin_df.to_excel(origin_writer)
        target_df.to_excel(target_writer)
        origin_writer.save()
        target_writer.save()


if __name__ == "__main__":
    PairGen(50000, headers_c=40, file_name="5w").gen_pair()
