from app import db
from models import Schedules, Bidan, Periode

class nsp():

    def generate_pattern_schedule(self, periode_date):
        periode_db = Periode.query.filter(Periode.periode == periode_date).first()
        last_periode = Periode.query.order_by(Periode.periode.desc()).filter(Periode.periode != periode_db.periode).first()
        bidan_schedule = Bidan.query\
                        .outerjoin(Schedules)\
                        .add_columns(Schedules.shift, Schedules.rest_shift, Bidan.officer, Bidan.id)\
                        .filter(Schedules.periode_id == last_periode.id).all()

        bidan_shift = {}
        for sch in bidan_schedule:
            if sch.shift:
                bidan_shift[sch.id] = sch.shift.split(",")
            else:
                bidan_shift[sch.id] = None

        #individu_next_shift = {'normal': [], 'static': []}
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

                # Schedules.update().values(rest_shift=temp).where(Schedules.periode_id == periode_db.id)

                # if temp:
                #     individu_next_shift['normal'].append({id: temp})
                # if temp_static:
                #     individu_next_shift['static'].append({id: temp_static})

                # sch = Schedules.query.get(id)
                # if Bidan.query.get(id).officer == "KT" or Bidan.query.get(id).officer == "KR":
                #     sch.rest_shift = temp_static
                # else:
                #     sch.rest_shift = temp
                # db.session.commit()


        # current_schedule = Schedules.query.join(Periode).add_columns(Schedules.rest_shift, Schedules.id).filter(
        #     Periode.periode == periode_date).all()
        # for csch in current_schedule:
        #     csch


    def save_rest_shift(self):
        pass


