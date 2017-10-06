from models import *

def first_data():
    first_periode = Periode()
    db.session.add(first_periode)
    db.session.commit()

    n = []
    n.append(Bidan(name='Asna', nip='', officer='KR', tim='tim'))
    n.append(Bidan(name='Sang ayu', nip='', officer='KT', tim='tim1'))
    n.append(Bidan(name='Ni Nyoman', nip='', officer='KT', tim='tim2'))
    n.append(Bidan(name='Tendri', nip='', officer='SN', tim='tim1'))
    n.append(Bidan(name='Novianti Toya', nip='', officer='JR', tim='tim1'))
    n.append(Bidan(name='Musdalifa', nip='', officer='JR', tim='tim1'))
    n.append(Bidan(name='Yuliana', nip='', officer='SN', tim='tim1'))
    n.append(Bidan(name='Rina', nip='', officer='JR', tim='tim1'))
    n.append(Bidan(name='Suriani', nip='', officer='JR', tim='tim1'))
    n.append(Bidan(name='Rebecca', nip='', officer='JR', tim='tim1'))
    n.append(Bidan(name='Helphin', nip='', officer='SN', tim='tim1'))
    n.append(Bidan(name='Eka Nurzam', nip='', officer='JR', tim='tim1'))
    n.append(Bidan(name='Linda', nip='', officer='SN', tim='tim2'))
    n.append(Bidan(name='Nurhaya', nip='', officer='JR', tim='tim2'))
    n.append(Bidan(name='Ni Ketut Purnama', nip='', officer='JR', tim='tim2'))
    n.append(Bidan(name='Ervina', nip='', officer='SN', tim='tim2'))
    n.append(Bidan(name='Susi Nurhayati', nip='', officer='JR', tim='tim2'))
    n.append(Bidan(name='Oktavia', nip='', officer='SN', tim='tim2'))
    n.append(Bidan(name='Zenab', nip='', officer='SN', tim='tim2'))
    n.append(Bidan(name='Nurlela', nip='', officer='JR', tim='tim2'))
    n.append(Bidan(name='Ervita', nip='', officer='JR', tim='tim2'))
    n.append(Bidan(name='Indah Rahmiya', nip='', officer='SN', tim='tim2'))
    n.append(Bidan(name='Novianti', nip='', officer='SN', tim='tim2'))
    n.append(Bidan(name='Dian Sari', nip='', officer='JR', tim='tim2'))
    n.append(Bidan(name='Imas', nip='', officer='JR', tim='tim2'))
    db.session.add_all(n)
    db.session.commit()

    n = []
    n.append(Schedules(name='Asna', nip='', officer='KR', tim='tim', bidan_id=1, periode_id=1,
                       shift='P,P,P,P,P,P,O,P,P,P,P,P,P,O,P,P,P,P,P,P,O,P,P,P,P,P,P,O,P,P'))
    n.append(Schedules(name='Sang ayu', nip='', officer='KT', tim='tim1', bidan_id=2, periode_id=1,
                       shift='P,P,P,P,P,P,O,P,P,P,P,P,P,O,P,P,P,P,P,P,O,P,P,P,P,P,P,O,P,P'))
    n.append(Schedules(name='Ni Nyoman', nip='', officer='KT', tim='tim2', bidan_id=3, periode_id=1,
                       shift='P,P,P,P,P,P,O,P,P,P,P,P,P,O,P,P,P,P,P,P,O,P,P,P,P,P,P,O,P,P'))
    n.append(Schedules(name='Tendri', nip='', officer='SN', tim='tim1', bidan_id=4, periode_id=1,
                       shift='S,S,S,S,S,O,S,S,O,M,M,O,O,S,S,O,S,M,M,O,O,P,M,M,O,O,P,P,P,P'))
    n.append(Schedules(name='Novianti Toya', nip='', officer='JR', tim='tim1', bidan_id=5, periode_id=1,
                       shift='S,S,O,O,O,S,S,O,S,S,O,S,S,O,M,M,O,O,M,M,O,O,M,M,O,O,M,M,O,O'))
    n.append(Schedules(name='Musdalifa', nip='', officer='JR', tim='tim1', bidan_id=6, periode_id=1,
                       shift='S,S,S,O,P,S,S,O,P,S,S,S,O,P,M,M,O,O,P,S,S,O,M,M,O,O,P,P,P,S'))
    n.append(Schedules(name='Yuliana', nip='', officer='SN', tim='tim1', bidan_id=7, periode_id=1,
                       shift='M,M,O,O,M,M,O,O,S,S,S,O,S,S,O,S,P,S,S,O,M,M,O,O,S,S,O,M,M,O'))
    n.append(Schedules(name='Rina', nip='', officer='JR', tim='tim1', bidan_id=8, periode_id=1,
                       shift='P,M,M,M,M,O,O,P,S,S,P,S,S,S,S,S,S,S,S,O,S,S,O,M,M,O,O,P,S,P'))
    n.append(Schedules(name='Suriani', nip='', officer='JR', tim='tim1', bidan_id=9, periode_id=1,
                       shift='S,S,S,O,O,M,M,O,O,M,M,O,O,S,S,S,O,P,S,S,O,S,S,S,O,S,P,P,P,S'))
    n.append(Schedules(name='Rebecca', nip='', officer='JR', tim='tim1', bidan_id=10, periode_id=1,
                       shift='M,M,O,O,S,S,O,S,S,O,S,S,O,M,M,O,O,P,P,M,M,O,O,S,M,M,O,O,S,S'))
    n.append(Schedules(name='Helphin', nip='', officer='SN', tim='tim1', bidan_id=11, periode_id=1,
                       shift='M,M,O,O,O,P,S,S,S,O,M,M,O,O,S,S,O,P,S,P,S,P,M,M,O,O,P,S,S,O'))
    n.append(Schedules(name='Eka Nurzam', nip='', officer='JR', tim='tim1', bidan_id=12, periode_id=1,
                       shift='M,M,O,M,M,O,O,M,M,O,O,P,P,M,M,O,O,S,M,M,O,O,P,S,S,O,S,S,O,M'))
    n.append(Schedules(name='Linda', nip='', officer='SN', tim='tim2', bidan_id=13, periode_id=1,
                       shift='S,P,S,M,O,O,S,S,S,S,S,O,P,S,S,S,O,M,M,O,O,P,S,S,M,M,O,O,P,P'))
    n.append(Schedules(name='Nurhaya', nip='', officer='JR', tim='tim2', bidan_id=14, periode_id=1,
                       shift='P,M,M,M,O,O,S,S,S,M,M,O,O,P,P,M,M,O,O,S,S,O,M,M,O,O,P,P,S,S'))
    n.append(Schedules(name='Ni Ketut Purnama', nip='', officer='JR', tim='tim2', bidan_id=15, periode_id=1,
                       shift='P,M,M,S,S,O,S,S,O,P,S,S,O,S,S,O,M,M,O,O,S,S,O,P,P,P,M,M,O,O'))
    n.append(Schedules(name='Ervina', nip='', officer='SN', tim='tim2', bidan_id=16, periode_id=1,
                       shift='S,S,O,O,S,M,M,O,O,S,S,O,S,S,O,M,M,O,O,M,M,O,O,S,S,O,S,S,S,O'))
    n.append(Schedules(name='Susi Nurhayati', nip='', officer='JR', tim='tim2', bidan_id=17, periode_id=1,
                       shift='P,P,P,O,O,P,M,M,O,O,P,S,M,M,O,O,P,P,S,S,O,S,S,O,P,S,S,P,P,P'))
    n.append(Schedules(name='Oktavia', nip='', officer='SN', tim='tim2', bidan_id=18, periode_id=1,
                       shift='S,S,S,M,O,O,M,M,O,O,M,M,O,O,S,M,M,O,O,M,M,O,O,P,S,S,M,M,O,O'))
    n.append(Schedules(name='Zenab', nip='', officer='SN', tim='tim2', bidan_id=19, periode_id=1,
                       shift='S,S,O,M,M,O,O,S,S,M,M,O,O,M,M,O,O,S,M,M,O,O,P,P,M,M,O,O,P,P'))
    n.append(Schedules(name='Nurlela', nip='', officer='JR', tim='tim2', bidan_id=20, periode_id=1,
                       shift='M,M,O,P,M,M,O,O,M,M,O,O,S,S,O,S,P,S,M,M,O,O,P,P,P,S,P,S,S,O'))
    n.append(Schedules(name='Ervita', nip='', officer='JR', tim='tim2', bidan_id=21, periode_id=1,
                       shift='S,S,O,O,M,M,O,O,M,M,O,O,S,S,O,S,S,S,O,S,S,O,M,M,O,O,S,S,O,P'))
    n.append(Schedules(name='Indah Rahmiya', nip='', officer='SN', tim='tim2', bidan_id=22, periode_id=1,
                       shift='P,S,P,M,M,O,O,S,S,S,S,O,M,M,O,O,S,S,O,P,M,M,O,O,P,S,S,O,M,M'))
    n.append(Schedules(name='Novianti', nip='', officer='SN', tim='tim2', bidan_id=23, periode_id=1,
                       shift='S,M,M,O,S,S,O,P,P,M,M,O,O,S,S,O,S,S,O,S,S,O,S,S,O,M,M,O,O,P'))
    n.append(Schedules(name='Dian Sari', nip='', officer='JR', tim='tim2', bidan_id=24, periode_id=1,
                       shift='M,M,O,M,M,O,O,S,S,S,P,S,S,O,M,M,O,O,S,S,O,P,P,S,S,O,M,M,O,O'))
    n.append(Schedules(name='Imas', nip='', officer='JR', tim='tim2', bidan_id=25, periode_id=1,
                       shift='P,P,M,M,O,O,P,M,M,O,O,M,M,O,O,S,S,O,M,M,O,O,P,S,S,O,P,P,M,M'))
    db.session.add_all(n)
    db.session.commit()