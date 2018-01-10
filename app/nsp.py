from app import db
from models import Schedules, Bidan, Periode
import random, operator, json
import timeit
import copy
import cPickle
from datetime import datetime

class Memetic():
    # shift = [['P'], ['S'], ['M']]
    shift = [['P','P','P','O'], ['S','S','O'], ['M','M','O','O']]
    hard_penalti = 5
    soft_penalti = 1

    def __init__(self, init_data):
        self.start_time = datetime.now()
        self.individu_static = {}
        self.bidan_w_schedule = {}
        self.lingkungan_individu = []
        self.temp_lingkungan_individu = []
        self.lingkungan_individu_fitness = []
        self.lingkungan_individu_fitness_interval = []
        self.elit_individu = {"fitness": 0, "individu": None}
        self.temp_total_pelanggaran = {"min_bidan": 0, "day_off": 0, "pairshift": 0, "working_hours": 0}
        self.min_jenis_shift = {
            "shift_pagi": {"sn": int(init_data["shift_pagi_sn"]), "jr": int(init_data["shift_pagi_jr"])},
            "shift_siang": {"sn": int(init_data["shift_siang_sn"]), "jr": int(init_data["shift_siang_jr"])},
            "shift_malam": {"sn": int(init_data["shift_malam_sn"]), "jr": int(init_data["shift_malam_jr"])}
        }
        self.hari = init_data["days"]
        self.periode_id = init_data["periode_id"]
        self.populasi = int(init_data["populasi"])
        self.generasi = int(init_data["generasi"])
        self.ahads = init_data["ahads"]
        self.probabilitas_mutasi = float(init_data["prob_mutasi"])
        self.probabilitas_rekombinasi = float(init_data["prob_rekombinasi"])
        self.probabilitas_local_search = float(init_data["prob_local_search"])
        self.get_pattern_schedule()

    def detail_solusi(self):
        print "FITNESS TERTINGGI: %f" % (self.elit_individu["fitness"])
        self.single_fitness(self.elit_individu["individu"], True)
        # self.print_individu(self.elit_individu["individu"])
        # self.single_fitness(self.elit_individu["individu"], True)


    def print_individu(self, individu):
        for pr in [1,2]:
            full_individu = dict(self.individu_static.items() + individu.items())
            for id, myindividu in full_individu.items():
                rest_shift = self.bidan_w_schedule[id]["rest_shift"]
                print id,
                if rest_shift != "CLEAR":
                    for index, shift in enumerate(rest_shift):
                        if shift == "-":
                            shift = full_individu[id][index]
                            if pr == 1:
                                print " %s [%s]" % (shift, self.bidan_w_schedule[id]["officer"]),
                            if pr == 2:
                                print " %s " % (shift),
                        else:
                            if pr == 1:
                                print " %s [%s][rest]" % (shift, self.bidan_w_schedule[id]["officer"]),
                            elif pr == 2:
                                print " %s " % (shift),

                else:
                    for shift in myindividu:
                        if pr == 1:
                            print " %s [%s]" % (shift, self.bidan_w_schedule[id]["officer"]),
                        if pr == 2:
                            print " %s " % (shift),

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


    def generate_random_shift(self, length=None):
        if length is None:
            length = self.hari
        shift_bidan = []
        while True:
            len_shift = len(self.shift) - 1
            rand_shift = random.randint(0, len_shift)
            shift_bidan = shift_bidan + self.shift[rand_shift]
            if len(shift_bidan) >= length:
                shift_bidan = shift_bidan[0:length]
                return shift_bidan


    # print(json.dumps(self.lingkungan_individu[0], indent=4, sort_keys=False))
    def initial_populasi(self):

        static_shift = []

        for d in range(self.hari):
            static_shift.append('P')

        for ahad in self.ahads:
            static_shift[ahad] = 'O'

        for i in range(self.populasi):
            individu = {}
            for bdn in Bidan.query.all():
                if bdn.officer == "SN" or bdn.officer == "JR":
                    individu[bdn.id] = self.generate_random_shift()
                else:
                    self.individu_static[bdn.id] = static_shift

            self.lingkungan_individu.append(individu)



    def min_bidan_shift_count(self, individu, hari):
        shift_count_result = {"shift_pagi": {"sn": 0, "jr": 0}, "shift_siang": {"sn": 0, "jr": 0}, "shift_malam": {"sn": 0, "jr": 0}}

        for id, bdn_w_sch in self.bidan_w_schedule.items():
            if bdn_w_sch["officer"] == "SN" or bdn_w_sch["officer"] == "JR":
                my_individu = individu
            else:
                my_individu = self.individu_static

            if bdn_w_sch["rest_shift"] != "CLEAR":
                shift = bdn_w_sch["rest_shift"][hari]
                if shift == "-":
                    shift = my_individu[id][hari]
                else:
                    shift = bdn_w_sch["rest_shift"][hari]
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
        total_pelanggaran = 0
        data = {}
        for hari in range(self.hari):
            pelanggaran = 0
            result = self.min_bidan_shift_count(individu, hari)
            jenis_shift = {"shift_pagi": "P", "shift_siang": "S", "shift_malam": "M"}
            for js, js_cell in jenis_shift.items():
                if result[js]["sn"] < self.min_jenis_shift[js]["sn"]:
                    if process == "fitness":
                        pelanggaran += 1
                    elif process == "improvement":
                        data['hari'] = hari
                        data['need_shift'] = js_cell
                        data['total_need'] = self.min_jenis_shift[js]['sn'] - result[js]['sn']
                        data['jenis'] = 'SN'
                        self.min_bidan_improve(individu, data)
                if result[js]["jr"] < self.min_jenis_shift[js]["jr"]:
                    melanggar = False
                    if result[js]["sn"] > self.min_jenis_shift[js]["sn"]:
                        total_result = result[js]['sn'] + result[js]['jr']
                        total_min = self.min_jenis_shift[js]["sn"] + self.min_jenis_shift[js]["jr"]
                        if total_result < total_min:
                            melanggar = True
                    else:
                        melanggar = True

                    if process == "fitness" and melanggar:
                        pelanggaran += 1
                    elif process == "improvement" and melanggar:
                        data['hari'] = hari
                        data['need_shift'] = js_cell
                        data['total_need'] = self.min_jenis_shift[js]['jr'] - self.min_jenis_shift[js]['jr']
                        data['jenis'] = 'JR'
                        self.min_bidan_improve(individu, data)

            if process == "fitness":
                total_pelanggaran += pelanggaran

            if debug:
                if pelanggaran > 0:
                    print "[MIN BIDAN] PELANGGARAN hari - %d" % (hari)
                    print "Pelanggaran: %d" % (pelanggaran)

        if debug:
            print "[MIN BIDAN] Total pelanggaran: %d" % (total_pelanggaran)

        if process == "fitness":
            return total_pelanggaran



    def min_bidan_improve(self, individu, data):
        bidan_id = self.bidan_w_schedule.keys()
        hari = data['hari']
        need_shift = data['need_shift']
        total_need = data['total_need']
        improve = True
        while improve:
            rand_id = random.randint(0, len(bidan_id) - 1)
            id = bidan_id[rand_id]
            restshift = self.bidan_w_schedule[id]['rest_shift']
            officer = self.bidan_w_schedule[id]["officer"]
            if officer != "KT" and officer != "KR" and officer != "persir":
                if data['jenis'] == officer or data['jenis'] == "JR":
                    if restshift != "CLEAR":
                        if restshift[hari] == "-":
                            shift = individu[id][hari]
                        else:
                            shift = None
                    else:
                        shift = individu[id][hari]

                    if shift is not None:
                        if hari + 1 <= self.hari - 1:
                            nextshift = individu[id][hari + 1]
                        else:
                            nextshift = "E"

                        if hari + 2 <= self.hari - 1:
                            next2shift = individu[id][hari + 2]
                        else:
                            next2shift = "E"

                        if hari + 3 <= self.hari - 1:
                            next3shift = individu[id][hari + 3]
                        else:
                            next3shift = "E"

                    if shift is not None:
                        if shift != need_shift:
                            individu[id][hari] = need_shift
                            if need_shift == "M":
                                if nextshift != "E":
                                    individu[id][hari + 1] = "M"
                                if next2shift != "E":
                                    individu[id][hari + 2] = "O"
                                if next3shift != "E":
                                    individu[id][hari + 3] = "O"
                            if need_shift == "S":
                                if nextshift != "E":
                                    individu[id][hari + 1] = "S"
                                if next2shift != "E":
                                    individu[id][hari + 2] = "O"


                            total_need = total_need - 1
                            if total_need <= 0:
                                improve = False


    def replace_shift(self, individu_row, hari, length_shift):
        shift_generate = self.generate_random_shift(length_shift)
        hari -= len(shift_generate) - 1
        for s in shift_generate:
            individu_row[hari] = s
            hari += 1


    def day_off(self, individu, process="fitness", debug=False):
        pelanggaran_total = 0
        for id, bdn_w_sch in self.bidan_w_schedule.items():

            pelanggaran_off_siang, pelanggaran_off_malam = 0, 0
            pelanggaran_off_day, pelanggaran_off = 0, 0
            siang, malam, pagi, off = 0, 0, 0, 0

            if bdn_w_sch["officer"] == "SN" or bdn_w_sch["officer"] == "JR":
                restshift = bdn_w_sch["rest_shift"]
                for hari in range(self.hari):
                    if restshift != "CLEAR":
                        if restshift[hari] == "-":
                            shift = individu[id][hari]
                            immutable_shift = None
                        else:
                            shift = restshift[hari]
                            immutable_shift = True

                    else:
                        shift = individu[id][hari]
                        immutable_shift = None

                    if shift is not None:
                        if hari + 1 <= self.hari - 1:
                            nextshift = individu[id][hari + 1]
                        else:
                            nextshift = "E"

                        if hari + 2 <= self.hari - 1:
                            next2shift = individu[id][hari + 2]
                        else:
                            next2shift = "E"

                        if hari + 3 <= self.hari - 1:
                            next3shift = individu[id][hari + 3]
                        else:
                            next3shift = "E"


                    if restshift != "CLEAR":
                        if hari + 1 <= self.hari - 1:
                            if restshift[hari + 1] != "-":
                                nextrestshift = restshift[hari + 1]
                            else:
                                nextrestshift = None
                        else:
                            nextrestshift = None

                        if hari + 2 <= self.hari - 1:
                            if restshift[hari + 2] != "-":
                                next2restshift = restshift[hari + 2]
                            else:
                                next2restshift = None
                        else:
                            next2restshift = None
                    else:
                        nextrestshift = None
                        next2restshift = None


                    if shift == "O":
                        siang, malam, pagi = 0, 0, 0
                        off += 1
                        if off > 2:
                            if process == "fitness":
                                pelanggaran_off += 1
                            elif process == "improvement":
                                individu[id][hari] = "P"
                            off = 0
                    elif shift == "P":
                        siang, malam, off = 0, 0, 0
                        pagi += 1

                        if pagi == 3:
                            if next2shift == "O":
                                if process == "fitness":
                                    pelanggaran_off_day += 1
                                elif process == "improvement":
                                    individu[id][hari + 2] = "P"

                            if nextrestshift is not None and immutable_shift is None:
                                if process == "fitness":
                                    pelanggaran_off_day += 1
                                elif process == "improvement":
                                    self.replace_shift(individu[id], hari, pagi)
                                pagi = 0
                            elif nextshift != "O" and nextshift != "E":
                                if process == "fitness":
                                    pelanggaran_off_day += 1
                                elif process == "improvement":
                                    individu[id][hari + 1] = "O"
                                pagi = 0
                        elif pagi < 3:
                            if nextshift == "O":
                                if process == "fitness":
                                    pelanggaran_off_day += 1
                                elif process == "improvement":
                                    individu[id][hari + 1] = "P"

                    elif shift == "S":
                        malam, off, pagi = 0, 0, 0
                        if siang == 0:
                            if nextrestshift is not None and next2restshift is not None and immutable_shift is None:
                                if nextrestshift == "S" and next2restshift == "S":
                                    if process == "fitness":
                                        pelanggaran_off_siang += 1
                                    elif process == "improvement":
                                        self.replace_shift(individu[id], hari, 1)
                            else:
                                if nextshift == "O":
                                    if process == "fitness":
                                        pelanggaran_off_siang += 1
                                    elif process == "improvement":
                                        individu[id][hari + 1] = "P"
                                else:
                                    siang += 1
                        elif siang == 1:
                            if nextrestshift is not None and immutable_shift is None:
                                if process == "fitness":
                                    pelanggaran_off_siang += 1
                                elif process == "improvement":
                                    self.replace_shift(individu[id], hari, 2)

                            elif nextshift != "O" and nextshift != "E":

                                if process == "fitness":
                                    pelanggaran_off_siang += 1
                                elif process == "improvement":
                                    individu[id][hari + 1] = "O"
                            elif next2shift == "O":

                                if process == "fitness":
                                    pelanggaran_off_siang += 1
                                elif process == "improvement":
                                    individu[id][hari + 2] = "P"
                            siang = 0
                        else:
                            siang += 1
                    elif shift == "M":
                        siang, off, pagi = 0, 0, 0
                        if malam == 0 and nextshift != "M" and nextshift != "E":
                            if nextrestshift is not None and immutable_shift is None:
                                if process == "fitness":
                                    pelanggaran_off_malam += 1
                                elif process == "improvement":
                                    self.replace_shift(individu[id], hari, 1)
                            else:
                                malam += 1
                                if process == "fitness":
                                    pelanggaran_off_malam += 1
                                elif process == "improvement":
                                    individu[id][hari + 1] = "M"
                                    if next2shift != "E":
                                        individu[id][hari + 2] = "O"

                                    if next3shift != "E":
                                        individu[id][hari + 3] = "O"

                        elif malam == 1:
                            if nextrestshift is not None and immutable_shift is None:
                                if process == "fitness":
                                    pelanggaran_off_malam += 1
                                elif process == "improvement":
                                    self.replace_shift(individu[id], hari, 2)

                            elif nextshift != "O" and nextshift != "E":
                                if process == "fitness":
                                    pelanggaran_off_malam += 1
                                elif process == "improvement":
                                    individu[id][hari + 1] = "O"

                            if next2restshift is not None and immutable_shift is None:
                                if process == "fitness":
                                    pelanggaran_off_malam += 1
                                elif process == "improvement":
                                    self.replace_shift(individu[id], hari, 3)

                            elif next2shift != "O" and next2shift != "E":
                                if process == "fitness":
                                    pelanggaran_off_malam += 1
                                elif process == "improvement":
                                    individu[id][hari + 2] = "O"

                            malam = 0
                        else:
                            malam += 1
                    else:
                        siang, malam, off, pagi = 0, 0, 0, 0

                pelanggaran_total += pelanggaran_off_malam + pelanggaran_off_siang + pelanggaran_off_day + pelanggaran_off

                if debug:
                    if pelanggaran_off > 0 or pelanggaran_off_day > 0 or pelanggaran_off_malam > 0 or pelanggaran_off_siang > 0:
                        print "[DAY OFF] PELANGGARAN BIDAN - %d" % (id)
                    if pelanggaran_off_siang > 0:
                        print "---S = %d" % (pelanggaran_off_siang)
                    if pelanggaran_off_malam > 0:
                        print "---M = %d" % (pelanggaran_off_malam)
                    if pelanggaran_off_day > 0:
                        print "---Off Day = %d" % (pelanggaran_off_day)
                    if pelanggaran_off > 0:
                        print "Off day kelebihan = %d" % (pelanggaran_off)

        if debug:
            print "[DAY OFF] Total Pelanggaran: %d" % (pelanggaran_total)

        if process == "fitness":
            return pelanggaran_total




    def pairshift_overflow(self, individu, process="fitness", debug=False):
        pelanggaran_total = 0
        for id, bdn_w_sch in self.bidan_w_schedule.items():
            pelanggaran, pair_shift_malam, pair_shift_siang = 0, 0, 0
            pelanggaran_pola_malam = 0
            malam, siang = 0, 0
            h = 0
            pair_patteran_malam = []
            if bdn_w_sch["officer"] == "SN" or bdn_w_sch["officer"] == "JR":
                restshift = bdn_w_sch["rest_shift"]
                for hari in range(self.hari):

                    if restshift != "CLEAR":
                        if restshift[hari] == "-":
                            shift = individu[id][hari]
                        else:
                            shift = restshift[hari]
                    else:
                        shift = individu[id][hari]

                    h += 1

                    if shift is not None:
                        if hari + 1 <= self.hari - 1:
                            nextshift = individu[id][hari + 1]
                        else:
                            nextshift = "E"

                    if shift == "M":
                        if nextshift == "M":
                            pair_patteran_malam.append([hari, hari+1])

                        malam += 1
                        siang = 0
                        if malam == 2:
                            pair_shift_malam += 1
                            if pair_shift_malam > 1 and h <= 7:
                                pair_shift_malam = 0
                                if process == "fitness":
                                    pelanggaran += 1
                                elif process == "improvement":
                                    self.replace_shift(individu[id], hari, 7)

                            malam = 0
                    elif shift == "S":
                        siang += 1
                        malam = 0
                        if siang == 2:
                            pair_shift_siang += 1
                            if pair_shift_siang > 1 and h <= 7:
                                pair_shift_siang = 0
                                if process == "fitness":
                                    pelanggaran += 1
                                elif process == "improvement":
                                    self.replace_shift(individu[id], hari, 7)
                            siang = 0
                    else:
                        malam = 0
                        siang = 0

                    if h == 7:
                        pair_shift_malam, pair_shift_siang= 0, 0
                        malam, siang = 0, 0
                        h = 0

            if len(pair_patteran_malam) > 3:
                if process == "fitness":
                    pelanggaran_pola_malam += 1
                elif process == "improvement":
                    generate_shift = self.generate_random_shift(2)
                    rand_index = random.randint(0, len(pair_patteran_malam)-1)
                    for i,index_hari in enumerate(pair_patteran_malam[rand_index]):
                        if restshift != "CLEAR":
                            if restshift[index_hari] == "-":
                                individu[id][index_hari] = generate_shift[i]
                        else:
                            individu[id][index_hari] = generate_shift[i]


            if debug:
                if pelanggaran > 0 or pelanggaran_pola_malam > 0:
                    print "[PAIR SHIFT] PELANGGARAN BIDAN - %d" % (id)
                if pelanggaran > 0:
                    print "Pelanggaran pair shift: %d" % (pelanggaran)
                if pelanggaran_pola_malam > 0:
                    print "Pelanggaran pola malam: %d" % (pelanggaran_pola_malam)

            pelanggaran_total += pelanggaran + pelanggaran_pola_malam

        if debug:
            print "[PAIR SHIFT] TOTAL PELANGGARAN: %d" % (pelanggaran_total)

        if process == "fitness":
            return pelanggaran_total



    def working_hours(self, individu, process="fitness", debug=False):
        pelanggaran_total = 0
        p, s, m = 6,6,12
        min_hours = 120
        max_hours = 180
        for id, bdn_w_sch in self.bidan_w_schedule.items():
            pelanggaran = 0
            if bdn_w_sch["officer"] == "SN" or bdn_w_sch["officer"] == "JR":
                restshift = bdn_w_sch["rest_shift"]
                total_jam = 0
                for hari in range(self.hari):
                    if restshift != "CLEAR":
                        if restshift[hari] == "-":
                            shift = individu[id][hari]
                        else:
                            shift = restshift[hari]
                    else:
                        shift = individu[id][hari]


                    if shift == "P":
                        total_jam = total_jam + p
                    elif shift == "S":
                        total_jam = total_jam + s
                    elif shift == "M":
                        total_jam = total_jam + m

                # print "[TOTAL_JAM] Bidan ke - %d adalah (%d)" % (id, total_jam)

                if total_jam < min_hours or total_jam > max_hours:
                    if process == "fitness":
                        pelanggaran = pelanggaran + 1
                    elif process == "improvement":
                        individu[id] = self.generate_random_shift()


            pelanggaran_total += pelanggaran

            if debug:
                if pelanggaran > 0:
                    print "[WORKING HOURS] PELANGGARAN BIDAN - %d" % (id)
                    print "Pelanggaran: %d" % (pelanggaran)


        if debug:
            print "[WORKING HOURS] TOTAL PELANGGARAN: %d" % (pelanggaran_total)

        if process == "fitness":
            return pelanggaran_total



    def fitness(self, debug=False):
        self.lingkungan_individu_fitness = []
        self.lingkungan_individu_fitness_interval = []
        total_fitness = 0
        for individu in self.lingkungan_individu:
            normalisasi_fitness = self.single_fitness(individu)
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


    def single_fitness(self, individu, debug=False):

        self.temp_total_pelanggaran["min_bidan"] = self.min_bidan(individu, "fitness", debug)
        self.temp_total_pelanggaran["day_off"] = self.day_off(individu, "fitness", debug)
        self.temp_total_pelanggaran["pairshift"] = self.pairshift_overflow(individu, "fitness", debug)
        self.temp_total_pelanggaran["working_hours"] = self.working_hours(individu, "fitness", debug)

        fitness = 0
        fitness += self.temp_total_pelanggaran["min_bidan"] * self.hard_penalti
        fitness += self.temp_total_pelanggaran["day_off"] * self.hard_penalti
        fitness += self.temp_total_pelanggaran["pairshift"] * self.soft_penalti
        fitness += self.temp_total_pelanggaran["working_hours"] * self.hard_penalti
        normalisasi_fitness = float(1) / (fitness+1)
        return normalisasi_fitness


    def roulette_wheel(self, rand_number):
        index = 0
        for fitness in self.lingkungan_individu_fitness_interval:
            if rand_number > fitness["awal"] and rand_number <= fitness["batas"]:
                return index
            index += 1


    def selection(self):
        self.parents_individu = []
        for i in range(len(self.lingkungan_individu)/2):
            p1 = self.roulette_wheel(random.uniform(0, 1))
            p2 = self.roulette_wheel(random.uniform(0, 1))
            parent1 = copy.deepcopy(self.lingkungan_individu[p1])
            parent2 = copy.deepcopy(self.lingkungan_individu[p2])
            self.parents_individu.append([parent1, parent2])


    def recombination(self):
        temp_linkungan_individu = []
        for parent in self.parents_individu:
            rand_val = random.uniform(0, 1)
            if rand_val <= self.probabilitas_rekombinasi:
                #REKOMBINASI ONE POINT COLUMN
                rand_col = random.randint(1, self.hari-1)
                parent1 = {"slice1": [], "slice2": []}
                parent2 = {"slice1": [], "slice2": []}
                anak1, anak2 = {}, {}


                for id, individu_row in parent[0].items():
                    parent1["slice1"].append(individu_row[0:rand_col])
                    parent1["slice2"].append(individu_row[rand_col:])

                for id, individu_row in parent[1].items():
                    parent2["slice1"].append(individu_row[0:rand_col])
                    parent2["slice2"].append(individu_row[rand_col:])

                index = 0
                for id, bdn_w_sch in self.bidan_w_schedule.items():
                    if bdn_w_sch["officer"] == "SN" or bdn_w_sch["officer"] == "JR":
                        anak1[id] = parent1["slice1"][index] + parent2["slice2"][index]
                        anak2[id] = parent2["slice1"][index] + parent1["slice2"][index]
                        index += 1

                temp_linkungan_individu.append(anak1)
                temp_linkungan_individu.append(anak2)
            else:
                temp_linkungan_individu.append(parent[0])
                temp_linkungan_individu.append(parent[1])

        del self.lingkungan_individu[:]
        self.lingkungan_individu = temp_linkungan_individu


    def mutation(self):

        for individu in self.lingkungan_individu:
            rand_value = random.uniform(0, 1)

            if rand_value <= self.probabilitas_mutasi:
                individu_id = individu.keys()
                for i in range(2):
                    rand_id = random.randint(0, len(individu_id) - 1)
                    id = individu_id[rand_id]
                    individu[id] = self.generate_random_shift()




    def local_search(self):
        for individu in self.lingkungan_individu:
            rand_value = random.uniform(0, 1)

            if rand_value < self.probabilitas_local_search:
                self.pairshift_overflow(individu, "improvement")

                self.working_hours(individu, "improvement")

                self.min_bidan(individu, "improvement")

                self.day_off(individu, "improvement")


    def elitist(self):
        i, value = max(enumerate(self.lingkungan_individu_fitness), key=operator.itemgetter(1))
        if value > self.elit_individu["fitness"]:
            self.elit_individu["fitness"] = value
            self.elit_individu["individu"] = copy.deepcopy(self.lingkungan_individu[i])

        total_remove = len(self.lingkungan_individu) - self.populasi
        total_remove += 1

        for i in range(total_remove):
            index, value = min(enumerate(self.lingkungan_individu_fitness), key=operator.itemgetter(1))
            del self.lingkungan_individu[index]
            del self.lingkungan_individu_fitness[index]

        elit = copy.deepcopy(self.elit_individu["individu"])
        self.lingkungan_individu.append(elit)


    def population_replacement(self):
        self.fitness()
        self.elitist()


    def termination(self, generasi):

        elit_fitness = self.single_fitness(self.elit_individu["individu"])
        totalp = 0
        for key, total in self.temp_total_pelanggaran.items():
            totalp += total

        end_time = datetime.now()
        elapsed = str(format(end_time - self.start_time))

        print "%d. %f" % (generasi, elit_fitness)
        print "----%d. %f" % (generasi, self.elit_individu["fitness"])
        print "Total Pelanggaran: %d" % totalp
        for jenis, total in self.temp_total_pelanggaran.items():
            print "---%s: %d" % (jenis, total)
        print "Waktu: %s" % elapsed
        print " "

        min_fitness = min(self.lingkungan_individu_fitness)
        max_fitness = max(self.lingkungan_individu_fitness)

        f = open('scheduling_process.txt', 'r')
        scheduling_process = f.read()
        msg = ""
        if scheduling_process == "false":
            print "PROSESS STOPED FROM CLIENT"
            print " "
            msg = "Stopped from client"
        elif min_fitness == max_fitness:
            print "TERMINASI TERPENUHI - KONVERGENSI FITNESS"
            print " "
            msg = "Konvergensi fitness"
            with open("scheduling_process.txt", "wb") as fo:
                fo.write("false")
        elif self.elit_individu["fitness"] == 1:
            print "TERMINASI TERPENUHI - TIDAK ADA PELANGGARAN"
            print " "
            msg = "Fitness sempurna"
        elif generasi < self.generasi-1:
            return {"stop": False}
        elif generasi == self.generasi-1:
            print "TERMINASI TERPENUHI - MAKSIMAL GENERASI TERCAPAI"
            print " "
            msg = "Maksimal generasi tercapai"
            with open("scheduling_process.txt", "wb") as fo:
                fo.write("false")
        elif generasi > self.generasi-3:
            unik = set(self.lingkungan_individu_fitness)
            unik_value = len(unik)
            print "UNIK FITNESS: %d" % (unik_value)
            return {"stop": False}

        result_individu = {}
        full_individu = dict(self.individu_static.items() + self.elit_individu["individu"].items())
        for id, myindividu in full_individu.items():
            rest_shift = self.bidan_w_schedule[id]["rest_shift"]
            result_individu[id] = []
            if rest_shift != "CLEAR":
                for index, shift in enumerate(rest_shift):
                    if shift == "-":
                        result_individu[id].append(full_individu[id][index])
                    else:
                        result_individu[id].append(shift)
            else:
                result_individu[id] = full_individu[id]

        # elapsed = timeit.default_timer() - self.start_time
        end_time = datetime.now()
        elapsed = str(format(end_time - self.start_time))


        data = {"individu": result_individu, "msg": msg, "generasi": generasi,
                "elit_fitness": self.elit_individu["fitness"],
                "pelanggaran": self.temp_total_pelanggaran, "total_pelanggaran": totalp, "execution_time": elapsed}

        return {"stop": True, "data": data}



def generate_pattern_schedule(periode_date, days):
    periode_db = Periode.query.filter(Periode.periode == periode_date).first()
    last_periode = Periode.query.order_by(Periode.periode.desc()).filter(Periode.periode < periode_db.periode).first()
    if last_periode:
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
        # print(json.dumps(last_periode.id, indent=4, sort_keys=False))
        for id, shift in bidan_shift.items():
            if not shift:
                temp = "CLEAR"
            else:
                index = len(shift) - 1
                temp_static = "CLEAR"
                if shift[index] == "P":
                    back = 0
                    pg = 0
                    start = True
                    while start:
                        if index >= back:
                            if shift[index - back] == "P":
                                pg += 1
                                back += 1
                            else:
                                start = False
                        else:
                            start = False

                    if Bidan.query.get(id).officer == "KT" or Bidan.query.get(id).officer == "KR" or Bidan.query.get(id).officer == "persir":
                        pola_pagi = 6
                        pola_pagi = pola_pagi - pg
                        rest = ["P" for i in range(pola_pagi)]
                        rest.append("O")
                        temp_static = ",".join(rest)
                        print temp_static
                    else:
                        if pg >= 3:
                            temp = "O"
                        else:
                            temp = "CLEAR"

                elif shift[index] == "S":
                    if index >= 1:
                        if shift[index - 1] == "S":
                            temp = "O"
                        else:
                            temp = "S,O"
                    else:
                        temp = "S,O"
                elif shift[index] == "M":
                    if index >= 1:
                        if shift[index - 1] == "M":
                            temp = "O,O"
                        else:
                            temp = "M,O,O"
                    else:
                        temp = "M,O,O"
                elif shift[index] == "O":
                    if index >= 1 and index >= 2:
                        if shift[index - 1] == "M" and shift[index - 2] == "M":
                            temp = "O"
                        else:
                            temp = "CLEAR"
                    else:
                        temp = "CLEAR"


                if Bidan.query.get(id).officer == "KT" or Bidan.query.get(id).officer == "KR" or Bidan.query.get(id).officer == "persir":
                    temps = temp_static
                else:
                    temps = temp


                if temps != "CLEAR":
                    temps_arr = temps.split(",")
                    none_rest = ["-" for i in range(days - len(temps_arr))]
                    none_rest_str = ",".join(none_rest)
                    temps = temps + "," + none_rest_str

                Schedules.query \
                    .filter((Schedules.periode_id == periode_db.id) & (Schedules.bidan_id == id)) \
                    .update({Schedules.rest_shift: temps})

                db.session.commit()
        return True
    else:
        return False
