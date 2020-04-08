"""Simulates the infection tree of a single patient"""

import random

def new_patient(status='I', nid=0):
    return {'status': status,
            'id': nid,
            'infected_by': None,
            'infects': [],
            'time': 0,
            'real_time': 0,
            'symptoms': False,
            'pd': 0}

def infection_tree(time, pi, pr, factor):
    """Creates an infection tree from a single infected patient.
    Patients are represented as dictionaries.
    status -> gives the state of a patient: ('I'): Infected - with probability pi
                                            ('R'): Recovered - with probability pr
                                            ('D'): Deceased - with probability pd
    id -> an identification number, helps to track who infected who.
    infected_by -> the id of who infected the patient
    infects -> a list of ids infected by the patient
    time -> a 'self' time, markes the progression of one patient disease
    real_time -> markes which iteration the patient gets infected
    symptoms -> bool, when the patient shows symptoms (True) it stops infecting
    (it is supposed that when someone starts to show symptoms they stay at home
    and stops infecting others)
    pd -> individual probability of death. As the illness progess in time if the
    patient does not recover, the probability of death raises."""

    patients = {}
    patient0 = new_patient()
    id_tracker = 0
    patients[id_tracker] = patient0

    for t in range(time):
        # list of new infected patients at time t
        list_of_new = []

        # update round
        for pt_id in patients:
            if patients[pt_id]['status'] == "I":
                patients[pt_id]['time'] += 1
                patients[pt_id]['pd'] = patients[pt_id]['time']/(factor*time)
                if patients[pt_id]['time'] >= 4 and patients[pt_id]['symptoms'] == False:
                    if random.random() < 0.5:
                        patients[pt_id]['symptoms'] = True

        # infection round
        for pt_id in patients:
            if patients[pt_id]['symptoms'] == False and patients[pt_id]['status'] == "I":
                if random.random() < pi:
                    id_tracker += 1
                    #print(f"patient {pt_id} infects {id_tracker}!")
                    #print(f"patient {pt_id} infected {patients[pt_id]['infects']}")
                    np = new_patient()
                    np['id'] = id_tracker
                    np['infected_by'] = patients[pt_id]['id']
                    patients[pt_id]['infects'].append(id_tracker)
                    list_of_new.append(np)

        # recovery round
        for pt_id in patients:
            if  patients[pt_id]['status'] == "I":
                if patients[pt_id]['time'] > 7:
                    if random.random() < pr:
                        patients[pt_id]['status'] = "R"
                        patients[pt_id]['symptoms'] = False

        # death round
        for pt_id in patients:
            if patients[pt_id]['symptoms'] == True and patients[pt_id]['status'] == "I":
                if random.random() < patients[pt_id]['pd']:
                    patients[pt_id]['status'] = "D"

        # add new patient to patients round
        for np in list_of_new:
            #print(np)
            patients[np['id']] = np

    return patients


