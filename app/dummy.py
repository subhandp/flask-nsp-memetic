from models import *
import datetime

def first_data():

    u = []
    u.append(User.create("subhandp","12345"))
    db.session.add_all(u)
    db.session.commit()

    fp = []
    fp.append(Periode(periode=datetime.date(2017, 9, 1)))
    db.session.add_all(fp)
    db.session.commit()

    n = []
    n.append(Bidan(name='Asna Beatrix P, S.ST', nip='197106291991012001', officer='KR', tim='none'))
    n.append(Bidan(name='Siti Marwa, SST', nip='197502192000122001', officer='KT', tim='tim1'))
    n.append(Bidan(name='Indotang , S.ST', nip='196906011989122002', officer='SN', tim='tim1'))
    n.append(Bidan(name='Emiliana, A.Md. Keb.', nip='198010192005022006', officer='SN', tim='tim1'))
    n.append(Bidan(name='Hasriati, A.Md. Keb', nip='198811092011012008', officer='JR', tim='tim1'))
    n.append(Bidan(name='Irta Ifriani, A.Md. Keb', nip='198704222011012009', officer='JR', tim='tim1'))
    n.append(Bidan(name='Ni Wayan Yus suami, A.Md. Keb', nip='198905212011012008', officer='JR', tim='tim1'))
    n.append(Bidan(name='Yeyen A.Paputugan, A.Md.Keb', nip='198801312011022001', officer='JR', tim='tim1'))
    n.append(Bidan(name='Vani Oktaviani, A.Md.Keb', nip='kontrak', officer='JR', tim='tim1'))
    n.append(Bidan(name='Sri Wulandari, A.Md.Keb', nip='kontrak', officer='JR', tim='tim1'))

    n.append(Bidan(name='Niluh Putriana, SST', nip='197806222005022004', officer='KT', tim='tim2'))
    n.append(Bidan(name='Risdawati, A.Md, Keb.', nip='197506202002122005', officer='SN', tim='tim2'))
    n.append(Bidan(name='Yuliana T, SST', nip='198612162009032008', officer='SN', tim='tim2'))
    n.append(Bidan(name='Yantie Sari Dewi E.Y, A.Md.Keb', nip='197607242007012031', officer='SN', tim='tim2'))
    n.append(Bidan(name='Ni Made Heri Susilawati, A.Md. Keb', nip='198208032006042014', officer='SN', tim='tim2'))
    n.append(Bidan(name='Sumarni, A.Md.Keb', nip='198211292010012005', officer='SN', tim='tim2'))
    n.append(Bidan(name='irm, A.Md.Keb', nip='198707232011012006', officer='JR', tim='tim2'))
    n.append(Bidan(name='Misrawati, A.Md.Kb', nip='198912102011012006', officer='JR', tim='tim2'))
    n.append(Bidan(name='Yuni Jehanita, A.Md.Keb', nip='198906052014022001', officer='JR', tim='tim2'))
    n.append(Bidan(name='Sylvia Ari Wahyuni, A.Md.Keb', nip='198801302015032001', officer='JR', tim='tim2'))

    n.append(Bidan(name='Jamila, SST', nip='197806122005022006', officer='KT', tim='tim3'))
    n.append(Bidan(name='Inda Rahimnya, S.Tr.Keb', nip='199011252011012003', officer='SN', tim='tim3'))
    n.append(Bidan(name='Nurlina S.ST', nip='198509092009022004', officer='SN', tim='tim3'))
    n.append(Bidan(name='Susi Nurhayati, Str.Keb', nip='198312052011012008', officer='JR', tim='tim3'))
    n.append(Bidan(name='Ni Nyoman Ekawati, A.Md.Keb', nip='198403052010012008', officer='SN', tim='tim3'))
    n.append(Bidan(name='Ni Kadek Susanti, A.Md.Keb', nip='198402172011012008', officer='JR', tim='tim3'))
    n.append(Bidan(name="Novita Ra'bung, A.Md.Keb", nip='198711212011012011', officer='JR', tim='tim3'))
    n.append(Bidan(name='Yunita Setianing Pratiwi, A.Md.Keb.', nip='198801202011012008', officer='JR', tim='tim3'))
    n.append(Bidan(name='Sri Wahyuni, A.Md.Keb', nip='kontrak', officer='JR', tim='tim3'))
    db.session.add_all(n)
    db.session.commit()

    n = []
    n.append(Schedules(bidan_id=1, periode_id=1, shift='O,O,O,P,P,P,P,P,P,O,P,P,P,P,P,P,O,P,P,P,P,P,P,O,P,P,P,P,P,P'))
    n.append(Schedules(bidan_id=2, periode_id=1, shift='O,O,O,P,P,P,P,P,P,O,P,P,P,P,P,P,O,P,P,P,P,P,P,O,P,P,P,P,P,P'))
    n.append(Schedules(bidan_id=3, periode_id=1, shift='O,O,O,P,P,P,P,P,P,O,P,P,P,P,P,P,O,P,P,P,P,P,P,O,P,P,P,P,P,P'))
    n.append(Schedules(bidan_id=4, periode_id=1, shift='P,P,P,O,P,P,M,M,O,O,P,P,P,P,O,S,S,L,M,M,O,O,P,P,P,P,O,S,S,S'))
    n.append(Schedules(bidan_id=5, periode_id=1, shift='O,O,S,S,O,O,O,O,O,S,S,O,M,M,O,O,P,P,S,L,S,S,O,M,M,O,O,P,P,P'))
    n.append(Schedules(bidan_id=6, periode_id=1, shift='O,O,M,M,O,O,P,P,P,P,P,S,S,O,M,M,O,O,P,S,P,O,P,P,S,O,M,M,O,O'))
    n.append(Schedules(bidan_id=7, periode_id=1, shift='O,S,O,P,P,P,P,P,O,P,M,M,O,O,P,P,P,P,O,P,P,M,M,O,O,P,P,P,P,P'))
    n.append(Schedules(bidan_id=8, periode_id=1, shift='O,O,P,P,P,O,S,S,S,O,M,M,O,O,P,P,O,S,P,P,O,P,P,O,M,M,O,O,P,S'))
    n.append(Schedules(bidan_id=9, periode_id=1, shift='O,O,P,P,S,S,O,P,M,M,O,O,P,P,P,O,P,S,S,O,M,M,O,O,P,P,S,O,P,P'))
    n.append(Schedules(bidan_id=10, periode_id=1, shift='O,O,P,P,YM,M,O,O,P,P,P,P,O,S,S,O,M,M,O,O,P,P,O,S,S,S,O,M,M'))

    n.append(Schedules(bidan_id=11, periode_id=1, shift='O,O,O,P,P,P,P,P,P,O,P,P,P,P,P,P,O,P,P,P,P,P,P,O,P,P,P,P,P,P'))
    n.append(Schedules(bidan_id=12, periode_id=1, shift='O,O,O,P,P,P,P,P,P,O,P,P,P,P,P,P,O,P,P,P,P,P,P,O,P,P,P,P,P,P'))
    n.append(Schedules(bidan_id=13, periode_id=1, shift='O,O,S,S,O,P,M,M,O,O,P,P,P,P,O,P,P,P,O,P,M,M,O,O,P,P,O,S,O,M'))
    n.append(Schedules(bidan_id=14, periode_id=1, shift='O,O,S,S,O,M,M,O,O,P,P,P,O,S,S,S,O,M,M,O,O,P,P,S,S,O,S,S,O,P'))
    n.append(Schedules(bidan_id=15, periode_id=1, shift='M,O,O,O,P,P,S,S,O,P,P,O,M,M,O,O,P,P,P,P,O,P,P,O,P,M,M,O,O,P'))
    n.append(Schedules(bidan_id=16, periode_id=1, shift='O,O,O,M,M,O,O,P,P,P,O,S,S,S,O,M,M,O,O,P,P,P,P,O,P,P,P,O,P,P'))
    n.append(Schedules(bidan_id=17, periode_id=1, shift='O,O,P,P,S,S,O,P,M,M,O,O,P,P,P,O,S,S,S,O,P,M,M,O,O,P,P,P,O,P'))
    n.append(Schedules(bidan_id=18, periode_id=1, shift='O,O,O,P,P,P,O,S,S,O,M,M,O,O,P,P,P,O,P,S,S,S,O,M,M,O,O,P,S,S'))
    n.append(Schedules(bidan_id=19, periode_id=1, shift='O,O,P,P,P,P,O,P,P,S,S,O,P,M,M,O,O,P,P,P,O,P,P,O,P,S,O,M,M,O'))
    n.append(Schedules(bidan_id=20, periode_id=1, shift='O,O,P,P,P,O,P,P,M,M,O,O,P,P,P,O,P,P,M,M,O,O,P,P,P,S,O,P,P,P'))

    n.append(Schedules(bidan_id=21, periode_id=1, shift='O,O,O,P,P,P,P,P,P,O,P,P,P,P,P,P,O,P,P,P,P,P,P,O,P,P,P,P,P,P'))
    n.append(Schedules(bidan_id=22, periode_id=1, shift='O,O,P,P,P,O,S,S,S,O,P,P,O,P,M,M,O,O,P,P,P,O,S,S,S,O,M,M,O,O'))
    n.append(Schedules(bidan_id=23, periode_id=1, shift='O,O,O,S,S,S,S,O,P,P,M,M,O,O,P,P,P,P,O,S,S,S,O,P,M,M,O,O,P,P'))
    n.append(Schedules(bidan_id=24, periode_id=1, shift='O,O,P,O,M,M,O,O,P,P,P,P,O,P,P,S,S,O,P,M,M,O,O,P,P,P,O,P,S,S'))
    n.append(Schedules(bidan_id=25, periode_id=1, shift='S,M,M,O,O,P,P,P,O,S,S,S,O,P,P,O,M,M,O,O,P,P,P,O,P,P,O,P,M,M'))
    n.append(Schedules(bidan_id=26, periode_id=1, shift='M,M,O,O,P,P,P,P,O,P,P,S,S,O,P,P,P,O,M,M,O,O,P,P,S,S,O,P,P,P'))
    n.append(Schedules(bidan_id=27, periode_id=1, shift='S,S,O,P,P,O,M,M,O,O,P,P,P,O,S,S,S,O,P,P,M,M,O,O,P,P,S,O,P,P'))
    n.append(Schedules(bidan_id=28, periode_id=1, shift='O,O,O,P,P,P,O,P,M,M,O,O,P,P,P,P,O,S,S,S,O,P,M,M,O,O,P,P,P,O'))
    n.append(Schedules(bidan_id=29, periode_id=1, shift='O,O,M,M,O,O,P,P,P,O,P,P,M,M,O,O,P,P,P,O,P,P,S,S,O,P,P,S,O,P'))

    db.session.add_all(n)
    db.session.commit()
