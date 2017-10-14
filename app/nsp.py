from app import db
from models import Schedules, Bidan, Periode
import random, operator, json

class Memetic():
    individu_static = {}
    bidan_w_schedule = {}
    lingkungan_individu = []
    temp_lingkungan_individu = []
    lingkungan_individu_fitness = []
    lingkungan_individu_fitness_interval = []
    elit_individu = {"fitness": 0, "individu": None, "total_elit": 2}
    shift = [['P'], ['S'], ['M']]
    hard_penalti = 5
    soft_penalti = 1

    def __init__(self, init_data):
        self.min_jenis_shift = {
            "shift_pagi": {"sn": int(init_data["shift_pagi_sn"]), "jr": int(init_data["shift_pagi_jr"])},
            "shift_siang": {"sn": int(init_data["shift_siang_sn"]), "jr": int(init_data["shift_siang_jr"])},
            "shift_malam": {"sn": int(init_data["shift_malam_sn"]), "jr": int(init_data["shift_malam_jr"])}
        }
        self.hari = init_data["days"]
        self.periode_id = init_data["periode_id"]
        self.populasi = int(init_data["populasi"])
        self.generasi = int(init_data["generasi"])
        self.probabilitas_mutasi = float(init_data["prob_mutasi"])
        self.probabilitas_rekombinasi = float(init_data["prob_rekombinasi"])
        self.probabilitas_local_search = float(init_data["prob_local_search"])
        self.get_pattern_schedule()

    def detail_solusi(self):
        print "FITNESS TERTINGGI: %f" % (self.elit_individu["fitness"])
        self.print_individu(self.elit_individu["individu"])
        self.single_fitness(self.elit_individu["individu"], True)

    def print_individu(self, individu):
        for pr in [1, 2]:
            full_individu = dict(self.individu_static.items() + individu.items())
            for id, myindividu in full_individu.items():
                rest_shift = self.bidan_w_schedule[id]["rest_shift"]
                print id,
                if rest_shift != "CLEAR":
                    for shift in rest_shift:
                        if pr == 1:
                            print " %s [%s/r]" % (shift, self.bidan_w_schedule[id]["officer"]),
                        elif pr == 2:
                            print " %s " % (shift),
                else:
                    rest_shift = []

                current_sch = self.hari - len(rest_shift)
                for i in range(current_sch):
                    if pr == 1:
                        print " %s [%s]" % (full_individu[id][i], self.bidan_w_schedule[id]["officer"]),
                    if pr == 2:
                        print " %s " % (full_individu[id][i]),
                print "\n\n"

            print "\n\n"



    def get_pattern_schedule(self):
        current_bidan_schedule = Schedules.query \
            .join(Bidan) \
            .add_columns(Bidan.id, Bidan.officer, Schedules.rest_shift) \
            .filter(Schedules.periode_id == self.periode_id).all()
        for bdn_sch in current_bidan_schedule:
            rest_shift = bdn_sch.rest_shift
            ''.join(rest_shift.split())
            if rest_shift != "CLEAR":
                rest_shift = rest_shift.split(",")
            self.bidan_w_schedule[bdn_sch.id] = {"officer": bdn_sch.officer, "rest_shift": rest_shift}


    def generate_random_shift(self):
        shift_bidan = []
        while True:
            len_shift = len(self.shift) - 1
            rand_shift = random.randint(0, len_shift)
            shift_bidan = shift_bidan + self.shift[rand_shift]
            if len(shift_bidan) >= self.hari:
                shift_bidan = shift_bidan[0:self.hari]
                return shift_bidan

    # print(json.dumps(self.lingkungan_individu[0], indent=4, sort_keys=False))
    def initial_populasi(self):
        static = ['P', 'P', 'P', 'P', 'P', 'P', 'O', 'P', 'P', 'P', 'P', 'P', 'P', 'O', 'P', 'P', 'P', 'P', 'P', 'P',
                  'O', 'P', 'P', 'P', 'P', 'P', 'P', 'O', 'P', 'P', 'P', 'P', 'P', 'P', 'O'];
        static_shift = static[0:self.hari]
        for i in range(self.populasi):
            individu = {}
            for bdn in Bidan.query.all():
                if bdn.officer == "SN" or bdn.officer == "JR":
                    individu[bdn.id] = self.generate_random_shift()
                else:
                    self.individu_static[bdn.id] = static_shift

            self.lingkungan_individu.append(individu)

        #self.print_individu(self.lingkungan_individu[0])


    def min_bidan_shift_count(self, individu, hari):
        shift_count_result = {"shift_pagi": {"sn": 0, "jr": 0}, "shift_siang": {"sn": 0, "jr": 0}, "shift_malam": {"sn": 0, "jr": 0}}

        for id, bdn_w_sch in self.bidan_w_schedule.items():
            if bdn_w_sch["officer"] == "SN" or bdn_w_sch["officer"] == "JR":
                my_individu = individu
            else:
                my_individu = self.individu_static

            if bdn_w_sch["rest_shift"] != "CLEAR":
                total_rest_shift = len(bdn_w_sch["rest_shift"])
                # jika 'hari' masih ada dalam 'rest shift'
                if total_rest_shift-1 >= hari:
                    shift = bdn_w_sch["rest_shift"][hari]
                else:
                    cur_hari = hari - total_rest_shift
                    shift = my_individu[id][cur_hari]
            else:
                shift = my_individu[id][hari]

            if shift == "P":
                if bdn_w_sch["officer"] == "SN" or bdn_w_sch["officer"] == "KT" or bdn_w_sch["officer"] == "KR":
                    shift_count_result["shift_pagi"]["sn"] += 1
                elif bdn_w_sch["officer"] == "JR":
                    shift_count_result["shift_pagi"]["jr"] += 1
            elif shift == "S":
                if bdn_w_sch["officer"] == "SN" or bdn_w_sch["officer"] == "KT" or bdn_w_sch["officer"] == "KR":
                    shift_count_result["shift_siang"]["sn"] += 1
                elif bdn_w_sch["officer"] == "JR":
                    shift_count_result["shift_siang"]["jr"] += 1
            elif shift == "M":
                if bdn_w_sch["officer"] == "SN" or bdn_w_sch["officer"] == "KT" or bdn_w_sch["officer"] == "KR":
                    shift_count_result["shift_malam"]["sn"] += 1
                elif bdn_w_sch["officer"] == "JR":
                    shift_count_result["shift_malam"]["jr"] += 1

        return shift_count_result

    def min_bidan(self, individu, process="fitness", debug=False):
        if process == "fitness":
            total_fitness = self.fitness_min_bidan(individu, debug)
            return total_fitness
        elif process == "improvement":
            individu = self.move_min_bidan(individu)
            return individu


    def fitness_min_bidan(self, individu, debug = False):
        total_pelanggaran = 0;
        for hari in range(self.hari):
            pelanggaran = 0
            result = self.min_bidan_shift_count(individu, hari)
            jenis_shift = ["shift_pagi", "shift_siang", "shift_malam"]
            for js in jenis_shift:
                if result[js]["sn"] < self.min_jenis_shift[js]["sn"]:
                    pelanggaran += 1
                elif result[js]["sn"] >= self.min_jenis_shift[js]["sn"]:
                    min_total = self.min_jenis_shift[js]["sn"] + self.min_jenis_shift[js]["jr"]
                    current_total = result[js]["sn"] + result[js]["jr"]
                    if current_total < min_total:
                        pelanggaran += 1

            total_pelanggaran += pelanggaran

            if debug:
                print "[MIN BIDAN] Pelanggaran hari - %d: (%d)" % (hari, pelanggaran)
                print "---P [SN] = %d, [JR] = %d" % (result["shift_pagi"]["sn"], result["shift_pagi"]["jr"])
                print "---S [SN] = %d, [JR] = %d" % (result["shift_siang"]["sn"], result["shift_siang"]["jr"])
                print "---M [SN] = %d, [JR] = %d" % (result["shift_malam"]["sn"], result["shift_malam"]["jr"])


        if debug:
            print "[MIN BIDAN] Total Pelanggaran: %d" % (total_pelanggaran)
        return total_pelanggaran


    def move_min_bidan(self, individu):
        for hari in range(self.hari):

            jenis_shift = {"shift_pagi": {"need": "P", "more1": "S", "more2": "M", "jenis_more1": "shift_siang",
                                          "jenis_more2": "shift_malam"},
                           "shift_siang": {"need": "S", "more1": "P", "more2": "M", "jenis_more1": "shift_pagi",
                                           "jenis_more2": "shift_malam"},
                           "shift_malam": {"need": "M", "more1": "P", "more2": "S", "jenis_more1": "shift_pagi",
                                           "jenis_more2": "shift_siang"}}

            for js_shift, js_shift_data in jenis_shift.items():
                result = self.min_bidan_shift_count(individu, hari)
                if result[js_shift]["sn"] < self.min_jenis_shift[js_shift]["sn"] or result[js_shift]["jr"] < self.min_jenis_shift[js_shift]["jr"]:

                    jenis_bidan = ["sn", "jr"]
                    for js_bidan in jenis_bidan:
                        result = self.min_bidan_shift_count(individu, hari)
                        if result[js_shift][js_bidan] < self.min_jenis_shift[js_shift][js_bidan]:
                            data = {"jenis": js_bidan.upper(), "hari": hari, "need": js_shift_data["need"], "more1": js_shift_data["more1"], "more2": js_shift_data["more2"],
                                    "need_min_shift": self.min_jenis_shift[js_shift][js_bidan],
                                    "need_current": result[js_shift][js_bidan],
                                    "shift_current_more1": result[js_shift_data["jenis_more1"]][js_bidan],
                                    "shift_min_more1": self.min_jenis_shift[js_shift_data["jenis_more1"]][js_bidan],
                                    "shift_current_more2": result[js_shift_data["jenis_more2"]][js_bidan],
                                    "shift_min_more2": self.min_jenis_shift[js_shift_data["jenis_more2"]][js_bidan]}

                            individu = self.move_min_bidan_improve(individu, data)
        return individu


    def move_min_bidan_improve(self, individu, data):
        total_more1, total_more2 = 0, 0
        total_need = data["need_min_shift"] - data["need_current"]

        if data["shift_current_more1"] > data["shift_min_more1"]:
            total_more1 = data["shift_current_more1"] - data["shift_min_more1"]
        if data["shift_current_more2"] > data["shift_min_more2"]:
            total_more2 = data["shift_current_more2"] - data["shift_min_more2"]

        jenis = data["jenis"]
        hari = data["hari"]
        shift_need = data["need"]
        shift_more1 = data["more1"]
        shift_more2 = data["more2"]
        for id, bdn_w_sch in self.bidan_w_schedule.items():
            jenis_bidan = bdn_w_sch["officer"]
            if jenis_bidan == "SN" or jenis_bidan == "JR":
                restshift = bdn_w_sch["rest_shift"]
                if restshift != "CLEAR":
                    if len(restshift)-1 < hari:
                        restshift_total = len(restshift)
                        cur_hari = hari - restshift_total
                    else:
                        cur_hari = None
                else:
                    cur_hari = None

                if cur_hari:
                    shift = individu[id][cur_hari]
                    if jenis_bidan == jenis:
                        if shift == shift_more1 and total_more1 > 0 and total_need > 0:
                            individu[id][cur_hari] = shift_need
                            individu[id][cur_hari-1] = "P"
                            total_more1 -= 1
                            total_need -= 1

                        if shift == shift_more2 and total_more2 > 0 and total_need > 0:
                            individu[id][cur_hari] = shift_need
                            individu[id][cur_hari-1] = "P"
                            total_more2 -= 1
                            total_need -= 1
                        #
                        # if shift == "O" and total_need > 0:
                        #     individu[id][cur_hari] = shift_need
                        #     individu[id][cur_hari-1] = "P"
                        #     individu[id][cur_hari-2] = "P"
                        #     total_need -= 1

        return individu


    def day_off(self, individu, process="fitness", debug=False):
        pelanggaran_total = 0
        for id, bdn_w_sch in self.bidan_w_schedule.items():

            pelanggaran_off_siang, pelanggaran_off_malam = 0, 0
            pelanggaran_off_day, pelanggaran_off = 0, 0
            siang, malam, off = 0, 0, 0

            if bdn_w_sch["officer"] == "SN" or bdn_w_sch["officer"] == "JR":
                restshift = bdn_w_sch["rest_shift"]
                for hari in range(self.hari):
                    if restshift != "CLEAR":
                        if len(restshift) - 1 >= hari:
                            shift = None
                        else:
                            total_restshift = len(restshift)
                            cur_hari = hari - total_restshift
                            shift = individu[id][cur_hari]
                    else:
                        cur_hari = hari
                        shift = individu[id][cur_hari]

                    if shift:
                        if hari + 1 <= self.hari - 1:
                            nextshift = individu[id][cur_hari + 1]
                        else:
                            nextshift = "E"

                        if hari + 2 <= self.hari - 1:
                            next2shift = individu[id][cur_hari + 2]
                        else:
                            next2shift = "E"

                    if shift == "O":
                        off += 1
                        siang = 0
                        malam = 0
                        if off > 2:

                            if process == "fitness":
                                pelanggaran_off += 1
                            elif process == "improvement":
                                individu[id][cur_hari] = "P"
                            off = 0
                    elif shift == "P":
                        siang = 0
                        malam = 0
                        off = 0
                        if nextshift == "O":

                            if process == "fitness":
                                pelanggaran_off_day += 1
                            elif process == "improvement":
                                individu[id][cur_hari + 1] = "P"
                    elif shift == "S":
                        malam = 0
                        off = 0
                        if siang == 0:
                            if nextshift == "O":

                                if process == "fitness":
                                    pelanggaran_off_siang += 1
                                elif process == "improvement":
                                    individu[id][cur_hari + 1] = "P"
                            else:
                                siang += 1
                        elif siang == 1:
                            if nextshift != "O" and nextshift != "E":

                                if process == "fitness":
                                    pelanggaran_off_siang += 1
                                elif process == "improvement":
                                    individu[id][cur_hari + 1] = "O"
                            elif next2shift == "O":

                                if process == "fitness":
                                    pelanggaran_off_siang += 1
                                elif process == "improvement":
                                    individu[id][cur_hari + 2] = "P"
                            siang = 0
                        else:
                            siang += 1
                    elif shift == "M":
                        siang = 0
                        off = 0
                        if malam == 0 and nextshift != "M" and nextshift != "E":
                            if nextshift == "O" and next2shift == "O":

                                if process == "fitness":
                                    pelanggaran_off_malam += 1
                                elif process == "improvement":
                                    individu[id][cur_hari + 2] = "P"
                            if nextshift != "O" and nextshift != "E":

                                if process == "fitness":
                                    pelanggaran_off_malam += 1
                                elif process == "improvement":
                                    individu[id][cur_hari + 1] = "O"
                                    malam = 0
                        elif malam == 1:
                            if nextshift == "O" and next2shift == "O" or nextshift == "E" or next2shift == "E":
                                nxt = None
                            else:

                                if process == "fitness":
                                    pelanggaran_off_malam += 1
                                elif process == "improvement":
                                    individu[id][cur_hari + 1] = "O"
                                    individu[id][cur_hari + 2] = "O"
                            malam = 0
                        else:
                            malam += 1
                    else:
                        siang = 0
                        malam = 0
                        off = 0

                pelanggaran_total += pelanggaran_off_malam + pelanggaran_off_siang + pelanggaran_off_day + pelanggaran_off

                if debug:
                    print "[DAY OFF] PELANGGARAN BIDAN - %d" % (id)
                    print "---S = %d" % (pelanggaran_off_siang)
                    print "---M = %d" % (pelanggaran_off_malam)
                    print "---Off Day = %d" % (pelanggaran_off_day)
                    print "Off day kelebihan = %d" % (pelanggaran_off)

        if debug:
            print "[DAY OFF] Total Pelanggaran: %d" % (pelanggaran_total)

        if process == "fitness":
            return pelanggaran_total
        elif process == "improvement":
            return individu



    def pairshift_overflow(self, individu, debug = False):
        pelanggaran_total = 0
        for id, bdn_w_sch in self.bidan_w_schedule.items():
            pelanggaran = 0
            malam = 0
            siang = 0
            pair_shift_malam = 0
            pair_shift_siang = 0
            h = 0
            if bdn_w_sch["officer"] == "SN" or bdn_w_sch["officer"] == "JR":
                restshift = bdn_w_sch["rest_shift"]
                for hari in range(self.hari):
                    if restshift != "CLEAR":
                        if len(restshift)-1 >= hari:
                            shift = None
                        else:
                            total_rest_shift = len(restshift)
                            cur_hari = hari - total_rest_shift
                            shift = individu[id][cur_hari]
                    else:
                        cur_hari = hari
                        shift = individu[id][cur_hari]

                    h += 1
                    if shift == "M":
                        malam += 1
                        siang = 0
                        if malam == 2:
                            pair_shift_malam += 1
                            if pair_shift_malam > 1 and h <= 7:
                                pair_shift_malam = 0
                                pelanggaran += 1
                            malam = 0
                    elif shift == "S":
                        siang += 1
                        malam = 0
                        if siang == 2:
                            pair_shift_siang += 1
                            if pair_shift_siang > 1 and h <= 7:
                                pair_shift_siang = 0
                                pelanggaran += 1
                            siang = 0
                    else:
                        malam = 0
                        siang = 0

                    if h == 7:
                        pair_shift_malam = 0
                        pair_shift_siang = 0
                        malam = 0
                        siang = 0
                        h = 0

            if debug:
                print "[PAIR SHIFT] PELANGGARAN BIDAN - %d" % (id)
                print "Pelanggaran: %d" % (pelanggaran)

            pelanggaran_total += pelanggaran

        if debug:
            print "[PAIR SHIFT] TOTAL PELANGGARAN: %d" % (pelanggaran_total)
        return pelanggaran_total


    def fitness(self, debug=False):
        self.lingkungan_individu_fitness = []
        self.lingkungan_individu_fitness_interval = []
        total_fitness = 0
        for individu in self.lingkungan_individu:
            fitness = 0
            fitness += self.min_bidan(individu, "fitness") * self.hard_penalti
            fitness += self.day_off(individu, "fitness") * self.hard_penalti
            fitness += self.pairshift_overflow(individu) * self.soft_penalti
            normalisasi_fitness = float(1) / (fitness+1)
            total_fitness += normalisasi_fitness
            self.lingkungan_individu_fitness.append(normalisasi_fitness)


        if debug:
            print(json.dumps(self.lingkungan_individu_fitness, indent=4, sort_keys=False))

        for index in range(len(self.lingkungan_individu_fitness)):
            self.lingkungan_individu_fitness_interval.append({"awal": 0, "batas": 0})
            if index-1 < 0:
                prev_key = 0
            else:
                prev_key = index-1
            batas_prev = self.lingkungan_individu_fitness_interval[prev_key]["batas"]
            awal = batas_prev
            batas = batas_prev + (self.lingkungan_individu_fitness[index]/total_fitness)
            self.lingkungan_individu_fitness_interval[index]["awal"] = awal
            self.lingkungan_individu_fitness_interval[index]["batas"] = batas

        # print "TOTAL FITNESS: %f" % (total_fitness)
        #
        # print "\n\n++++++++++++++++++++++++START IMPROVEMENT+++++++++++++++++++++++++++\n\n"
        # self.print_individu(self.lingkungan_individu[0])
        # self.single_fitness(self.lingkungan_individu[0], True)
        # print "\n\n++++++++++++++++++++++++IMPROVEMENT+++++++++++++++++++++++++++\n\n"
        # ip = self.min_bidan(self.lingkungan_individu[0], "improvement", debug)
        # self.print_individu(ip)
        # self.single_fitness(ip, True)


    def single_fitness(self, individu, debug=False):
        fitness = 0
        fitness += self.min_bidan(individu, "fitness", debug) * self.hard_penalti
        fitness += self.day_off(individu, "fitness", debug) * self.hard_penalti
        fitness += self.pairshift_overflow(individu, debug) * self.soft_penalti
        normalisasi_fitness = float(1) / (fitness+1)
        return normalisasi_fitness


    def roulette_wheel(self, rand_number):
        index = 0
        for fitness in self.lingkungan_individu_fitness_interval:
            if rand_number >= fitness["awal"] and rand_number <= fitness["batas"]:
                return index
            index += 1


    def selection(self):
        self.parents_individu = []
        for i in range(len(self.lingkungan_individu)/2):
            parent1 = self.roulette_wheel(random.uniform(0, 1))
            parent2 = self.roulette_wheel(random.uniform(0, 1))
            self.parents_individu.append([parent1, parent2])
        # print len(self.parents_individu)
        # print(json.dumps(self.parents_individu, indent=4, sort_keys=False))



    def recombination(self):
        for parent in self.parents_individu:
            rand_val = random.uniform(0, 1)
            if rand_val <= self.probabilitas_rekombinasi:
                #REKOMBINASI ONE POINT COLUMN
                rand_col = random.randint(1, self.hari-1)
                parent1 = {"slice1": [], "slice2": []}
                parent2 = {"slice1": [], "slice2": []}
                anak1, anak2 = {}, {}


                for id, individu_row in self.lingkungan_individu[parent[0]].items():
                    parent1["slice1"].append(individu_row[0:rand_col])
                    parent1["slice2"].append(individu_row[rand_col:])

                for id, individu_row in self.lingkungan_individu[parent[1]].items():
                    parent2["slice1"].append(individu_row[0:rand_col])
                    parent2["slice2"].append(individu_row[rand_col:])

                index = 0
                for id, bdn_w_sch in self.bidan_w_schedule.items():
                    if bdn_w_sch["officer"] == "SN" or bdn_w_sch["officer"] == "JR":
                        anak1[id] = parent1["slice1"][index] + parent2["slice2"][index]
                        anak2[id] = parent2["slice1"][index] + parent1["slice2"][index]
                        index += 1

                self.temp_lingkungan_individu.append(anak1)
                self.temp_lingkungan_individu.append(anak2)
            else:
                self.temp_lingkungan_individu.append(self.lingkungan_individu[parent[0]])
                self.temp_lingkungan_individu.append(self.lingkungan_individu[parent[1]])


    def mutation(self):
        for individu_index in range(len(self.temp_lingkungan_individu)):
            rand_value = random.uniform(0, 1)
            if rand_value <= self.probabilitas_mutasi:
                kind = random.randint(0, 1)
                if kind == 0:
                    rand_col = random.randint(0, self.hari-1)
                    rand_col_val = ["P", "S", "M"]
                    for id, individu in self.temp_lingkungan_individu[individu_index].items():
                        index_col = random.randint(0, len(rand_col_val) - 1)
                        mutation_col = rand_col_val[index_col]
                        self.temp_lingkungan_individu[individu_index][id][rand_col] = mutation_col
                elif kind == 1:
                    individu_id = self.temp_lingkungan_individu[individu_index].keys()
                    rand_id = random.randint(0, len(individu_id) - 1)
                    id = individu_id[rand_id]
                    self.temp_lingkungan_individu[individu_index][id] = self.generate_random_shift()


    def local_search(self):
        for index in range(len(self.temp_lingkungan_individu)):
                rand_value = random.uniform(0, 1)
                if rand_value < self.probabilitas_local_search:
                    individu = self.temp_lingkungan_individu[index]
                    current_fitness = self.single_fitness(individu)

                    individu_improvement = self.min_bidan(individu, "improvement")
                    individu_improvement = self.day_off(individu_improvement, "improvement")

                    fitness_improvement = self.single_fitness(individu_improvement)

                    if fitness_improvement > current_fitness:
                        individu = individu_improvement

                    self.temp_lingkungan_individu[index] = individu


    def elitist(self):
        # 'key' adalah pembanding fungsi max()
        # 'itemgetter(1)' mengambil index 1 dari 'enumerate' sebagai pembanding
        index, value = max(enumerate(self.lingkungan_individu_fitness), key=operator.itemgetter(1))
        if self.elit_individu["fitness"] < value:
            self.elit_individu["fitness"] = value
            self.elit_individu["individu"] = self.lingkungan_individu[index]
        #REMOVE WORSE INDIVIDU
        total_remove = len(self.lingkungan_individu_fitness) - self.populasi
        total_remove += self.elit_individu["total_elit"]

        # fitness_sort_asc = sorted(range(len(self.lingkungan_individu_fitness)), key=lambda k: self.lingkungan_individu_fitness[k])
        # remove_individu = fitness_sort_asc[0:total_remove]
        # lf = len(self.lingkungan_individu_fitness)
        # ll = len(self.lingkungan_individu)
        # print "%d - %d" % (lf, ll)
        # print remove_individu
        # for index in remove_individu:
        #     del self.lingkungan_individu[index]

        for i in range(total_remove):
            index, value = min(enumerate(self.lingkungan_individu_fitness), key=operator.itemgetter(1))
            del self.lingkungan_individu[index]
            del self.lingkungan_individu_fitness[index]

        for i in range(self.elit_individu["total_elit"]):
            self.lingkungan_individu.append(self.elit_individu["individu"])


    def population_replacement(self):
        self.lingkungan_individu = self.temp_lingkungan_individu
        self.temp_lingkungan_individu = []
        self.fitness()
        self.elitist()
        # print(json.dumps(self.elit_individu, indent=4, sort_keys=False))

    def termination(self, generasi):
        print "%d. %f" % (generasi, self.elit_individu["fitness"])

        min_fitness = min(self.lingkungan_individu_fitness)
        max_fitness = max(self.lingkungan_individu_fitness)

        f = open('scheduling_process.txt', 'r')
        scheduling_process = f.read()

        if scheduling_process == "false":
            print "PROSESS STOPED FROM CLIENT"
            return True
        if min_fitness == max_fitness:
            print "TERMINASI TERPENUHI - KONVERGENSI FITNESS"
            return True
        elif self.elit_individu["fitness"] == 1:
            print "TERMINASI TERPENUHI - TIDAK ADA PELANGGARAN"
            return True
        elif generasi > self.generasi-3:
            unik = set(self.lingkungan_individu_fitness)
            unik_value = len(unik)
            print "UNIK FITNESS: %d" % (unik_value)
            return False


def generate_pattern_schedule(periode_date):
    periode_db = Periode.query.filter(Periode.periode == periode_date).first()
    last_periode = Periode.query.order_by(Periode.periode.desc()).filter(Periode.periode != periode_db.periode).first()
    bidan_schedule = Bidan.query \
        .outerjoin(Schedules) \
        .add_columns(Schedules.shift, Schedules.rest_shift, Bidan.officer, Bidan.id) \
        .filter(Schedules.periode_id == last_periode.id).all()

    bidan_shift = {}
    for sch in bidan_schedule:
        if sch.shift:
            bidan_shift[sch.id] = sch.shift.split(",")
        else:
            bidan_shift[sch.id] = None

    for id, shift in bidan_shift.items():
        index = len(shift) - 1
        if not shift:
            temp = "CLEAR"
        else:
            if shift[index] == "P":
                back = 0
                pg = 0
                start = True
                while start:
                    if shift[index - back] == "P":
                        pg += 1
                        back += 1
                    else:
                        start = False

                if Bidan.query.get(id).officer == "KT" or Bidan.query.get(id).officer == "KR":
                    pola_pagi = 6
                    pola_pagi = pola_pagi - pg
                    rest = ["P" for i in range(pola_pagi)]
                    rest.append("O")
                    temp_static = ",".join(rest)
                else:
                    pola_pagi = 3
                    pola_pagi = pola_pagi - pg
                    if pola_pagi > 0:
                        rest = ["P" for i in range(pola_pagi)]
                        temp = ",".join(rest)
                    else:
                        temp = "CLEAR"

            elif shift[index] == "S":
                if shift[index - 1] == "S":
                    temp = "O"
                else:
                    temp = "S,O"
            elif shift[index] == "M":
                if shift[index - 1] == "M":
                    temp = "O,O"
                else:
                    temp = "M,O,O"
            elif shift[index] == "O":
                if shift[index - 1] == "M" and shift[index - 2] == "M":
                    temp = "O"
                else:
                    temp = "CLEAR"

            if Bidan.query.get(id).officer == "KT" or Bidan.query.get(id).officer == "KR":
                Schedules.query \
                    .filter((Schedules.periode_id == periode_db.id) & (Schedules.bidan_id == id)) \
                    .update({Schedules.rest_shift: temp_static})
            else:
                Schedules.query \
                    .filter((Schedules.periode_id == periode_db.id) & (Schedules.bidan_id == id)) \
                    .update({Schedules.rest_shift: temp})

            db.session.commit()
