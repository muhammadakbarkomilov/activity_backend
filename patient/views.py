import os
from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from .models import PatientData
from .forms import PatientDataForm
import openpyxl
from openpyxl.utils import get_column_letter
from django.http import HttpResponse
from django.db.models import Q


def edit_patient(request, pk):
    patient = get_object_or_404(PatientData, pk=pk)
    if request.method == 'POST':
        form = PatientDataForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, "Bemor ma'lumotlari muvaffaqiyatli o'zgartirildi!")
            return redirect('patients')
    else:
        form = PatientDataForm(instance=patient)

    return render(request, 'edit_patient.html', {
        'form': form,
        'patient': patient
    })


def index(request):
    if request.method == 'POST':
        form = PatientDataForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patients')
    else:
        form = PatientDataForm()
    return render(request, 'index.html', {'form': form})

# def patients(request):
#     all_patients = PatientData.objects.all().order_by('-created_at')
#     return render(request, 'patients.html', {'patients': all_patients})


def patients(request):
    # Barcha bemorlarni olish
    patients_list = PatientData.objects.all().order_by('-created_at')

    # Qidiruv parametri
    search_query = request.GET.get('q')
    if search_query:
        patients_list = patients_list.filter(
            Q(full_name__icontains=search_query) |
            Q(telephone__icontains=search_query) |
            Q(id__icontains=search_query)
        )

    # Saralash parametri
    sort_by = request.GET.get('sort')
    if sort_by == 'name_asc':
        patients_list = patients_list.order_by('full_name')
    elif sort_by == 'name_desc':
        patients_list = patients_list.order_by('-full_name')
    elif sort_by == 'date_asc':
        patients_list = patients_list.order_by('created_at')
    elif sort_by == 'date_desc':
        patients_list = patients_list.order_by('-created_at')
    else:
        # Standart tartib
        patients_list = patients_list.order_by('-created_at')

    # Paginatsiya
    paginator = Paginator(patients_list, 10)  # Har sahifada 10 ta bemor
    page_number = request.GET.get('page')
    patients = paginator.get_page(page_number)

    context = {
        'patients': patients,
    }
    return render(request, 'patients.html', context)

def export_selected_excel(request):
    global patient
    if request.method == 'POST':
        selected_id = request.POST.get('selected_patient')
        patients = PatientData.objects.filter(id=selected_id)

        try:
            template_path = os.path.join(settings.BASE_DIR, 'patient/templates', 'patient-exel.xlsx')
            workbook = openpyxl.load_workbook(template_path)
            sheet = workbook['Лист2']

            # Helper function to safely write to merged cells
            def write_safe(cell, value):
                if value is None:
                    value = ''
                for merged_range in sheet.merged_cells.ranges:
                    if cell.coordinate in merged_range:
                        sheet[merged_range.min_row][merged_range.min_col - 1].value = value
                        return
                sheet[cell.coordinate] = value

            start_row = 3  # Starting row (e.g., row 3)
            for idx, patient in enumerate(patients, start=0):
                row = start_row + idx

                # Basic patient information
                sheet[f'A1'] = f"Patient registration card № {patient.reg_no}" or 'no'
                sheet[f'A3'] = patient.history_t if patient.history_t else 'no'
                sheet[f'D3'] = patient.full_name or 'no'
                sheet[f'L3'] = patient.date_of_birth.strftime('%d.%m.%Y') if patient.date_of_birth else 'no'
                sheet[f'P3'] = patient.address if patient.address else 'no'
                sheet[f'AC3'] = patient.telephone if patient.telephone else 'no'
                sheet[f'AH3'] = patient.date_of_examination if patient.date_of_examination else 'no'
                if patient.consanguineous_marriage_description:
                    sheet[f'E4'] = patient.consanguineous_marriage if patient.consanguineous_marriage else 'no'
                    sheet[f'E5'] = patient.consanguineous_marriage_description if patient.consanguineous_marriage_description else 'no'

                if patient.hereditary_diseases:
                    sheet[f'E6'] = patient.hereditary_diseases if patient.hereditary_diseases else 'no'
                    sheet[f'E7'] = patient.hereditary_diseases_description if patient.hereditary_diseases_description else 'no'

                if patient.gestation_period == "28-19":
                    sheet[f'O7'] = "yes" if patient.gestation_period else 'no'
                elif patient.gestation_period == "30-31":
                    sheet[f'P7'] = "yes" if patient.gestation_period else 'no'
                elif patient.gestation_period == "32-33":
                    sheet[f'Q7'] = "yes" if patient.gestation_period else 'no'
                elif patient.gestation_period == "34-35":
                    sheet[f'R7'] = "yes" if patient.gestation_period else 'no'
                elif patient.gestation_period == "36-37":
                    sheet[f'S7'] = "yes" if patient.gestation_period else 'no'
                elif patient.gestation_period == "38-39":
                    sheet[f'T7'] = "yes" if patient.gestation_period else 'no'
                elif patient.gestation_period == "40-41":
                    sheet[f'U7'] = "yes" if patient.gestation_period else 'no'

                if patient.pregnancy_number == 1:
                    sheet[f'T4'] = "yes" if patient.pregnancy_number else 'no'
                elif patient.pregnancy_number == 2:
                    sheet[f'V4'] = "yes" if patient.pregnancy_number else 'no'
                elif patient.pregnancy_number == 3:
                    sheet[f'X4'] = "yes" if patient.pregnancy_number else 'no'
                elif patient.pregnancy_number == 4:
                    sheet[f'Z4'] = "yes" if patient.pregnancy_number else 'no'
                elif patient.pregnancy_number == 5:
                    sheet[f'AB4'] = "yes" if patient.pregnancy_number else 'no'
                elif patient.pregnancy_number == 6:
                    sheet[f'AD4'] = "yes" if patient.pregnancy_number else 'no'
                elif patient.pregnancy_number == 7:
                    sheet[f'AF4'] = "yes" if patient.pregnancy_number else 'no'
                elif patient.pregnancy_number == 8:
                    sheet[f'AH4'] = "yes" if patient.pregnancy_number else 'no'
                elif patient.pregnancy_number == 9:
                    sheet[f'AJ4'] = "yes" if patient.pregnancy_number else 'no'

                if patient.childbirth_number == 1:
                    sheet[f'T5'] = "yes" if patient.childbirth_number else 'no'
                elif patient.childbirth_number == 2:
                    sheet[f'V5'] = "yes" if patient.childbirth_number else 'no'
                elif patient.childbirth_number == 3:
                    sheet[f'X5'] = "yes" if patient.childbirth_number else 'no'
                elif patient.childbirth_number == 4:
                    sheet[f'Z5'] = "yes" if patient.childbirth_number else 'no'
                elif patient.childbirth_number == 5:
                    sheet[f'AB5'] = "yes" if patient.childbirth_number else 'no'
                elif patient.childbirth_number == 6:
                    sheet[f'AD5'] = "yes" if patient.childbirth_number else 'no'
                elif patient.childbirth_number == 7:
                    sheet[f'AF5'] = "yes" if patient.childbirth_number else 'no'
                elif patient.childbirth_number == 8:
                    sheet[f'AH5'] = "yes" if patient.childbirth_number else 'no'
                elif patient.childbirth_number == 9:
                    sheet[f'AJ5'] = "yes" if patient.childbirth_number else 'no'

                sheet[f'F11'] = "yes" if patient.rapid_labor else 'no'
                sheet[f'F12'] = "yes" if patient.protracted_labor else 'no'
                sheet[f'F13'] = "yes" if patient.weakness_occupation else 'no'
                sheet[f'F14'] = "yes" if patient.placental_abruption else 'no'
                sheet[f'F15'] = "yes" if patient.increased_blood_pressure else 'no'
                sheet[f'F16'] = "yes" if patient.post_term else 'no'
                sheet[f'F17'] = "yes" if patient.preterm else 'no'

                sheet[f'L11'] = "yes" if patient.first_half_medication else 'no'
                sheet[f'L12'] = "yes" if patient.first_half_toxicosis else 'no'
                sheet[f'L13'] = "yes" if patient.first_half_threatened_miscarriage else 'no'
                sheet[f'L14'] = "yes" if patient.first_half_arv else 'no'
                sheet[f'L15'] = "yes" if patient.first_half_stress else 'no'
                sheet[f'L16'] = "yes" if patient.first_half_anemia else 'no'
                sheet[f'L17'] = "yes" if patient.first_half_rh_incompatibility else 'no'
                sheet[f'N11'] = patient.first_half_medication_description if patient.first_half_medication_description else 'no'

                sheet[f'T11'] = "yes" if patient.second_half_medication else 'no'
                sheet[f'T12'] = "yes" if patient.second_half_toxicosis else 'no'
                sheet[f'T13'] = "yes" if patient.second_half_threatened_miscarriage else 'no'
                sheet[f'T14'] = "yes" if patient.second_half_arv else 'no'
                sheet[f'T15'] = "yes" if patient.second_half_stress else 'no'
                sheet[f'T16'] = "yes" if patient.second_half_anemia else 'no'
                sheet[f'T17'] = "yes" if patient.second_half_rh_incompatibility else 'no'
                sheet[f'X11'] = patient.second_half_medication_description if patient.second_half_medication_description else 'no'

                if patient.mother_age_at_birth == "15-17":
                    sheet[f'I18'] = "yes" if patient.mother_age_at_birth else 'no'
                elif patient.mother_age_at_birth == "18-20":
                    sheet[f'K18'] = "yes" if patient.mother_age_at_birth else 'no'
                elif patient.mother_age_at_birth == "21-23":
                    sheet[f'M18'] = "yes" if patient.mother_age_at_birth else 'no'
                elif patient.mother_age_at_birth == "24-26":
                    sheet[f'O18'] = "yes" if patient.mother_age_at_birth else 'no'
                elif patient.mother_age_at_birth == "27-29":
                    sheet[f'Q18'] = "yes" if patient.mother_age_at_birth else 'no'
                elif patient.mother_age_at_birth == "30-32":
                    sheet[f'S18'] = "yes" if patient.mother_age_at_birth else 'no'
                elif patient.mother_age_at_birth == "33-35":
                    sheet[f'U18'] = "yes" if patient.mother_age_at_birth else 'no'
                elif patient.mother_age_at_birth == "36-38":
                    sheet[f'W18'] = "yes" if patient.mother_age_at_birth else 'no'
                elif patient.mother_age_at_birth == "39-40":
                    sheet[f'Y18'] = "yes" if patient.mother_age_at_birth else 'no'
                elif patient.mother_age_at_birth == "40-42":
                    sheet[f'AZ18'] = "yes" if patient.mother_age_at_birth else 'no'
                elif patient.mother_age_at_birth == "43-45":
                    sheet[f'BB18'] = "yes" if patient.mother_age_at_birth else 'no'
                elif patient.mother_age_at_birth == "46-48":
                    sheet[f'DD18'] = "yes" if patient.mother_age_at_birth else 'no'
                elif patient.mother_age_at_birth == "49-50":
                    sheet[f'FF18'] = "yes" if patient.mother_age_at_birth else 'no'

                if patient.father_age_at_birth == "15-17":
                    sheet[f'I19'] = "yes" if patient.father_age_at_birth else 'no'
                elif patient.father_age_at_birth == "18-20":
                    sheet[f'K19'] = "yes" if patient.father_age_at_birth else 'no'
                elif patient.father_age_at_birth == "21-23":
                    sheet[f'M19'] = "yes" if patient.father_age_at_birth else 'no'
                elif patient.father_age_at_birth == "24-26":
                    sheet[f'O19'] = "yes" if patient.father_age_at_birth else 'no'
                elif patient.father_age_at_birth == "27-29":
                    sheet[f'Q19'] = "yes" if patient.father_age_at_birth else 'no'
                elif patient.father_age_at_birth == "30-32":
                    sheet[f'S19'] = "yes" if patient.father_age_at_birth else 'no'
                elif patient.father_age_at_birth == "33-35":
                    sheet[f'U19'] = "yes" if patient.father_age_at_birth else 'no'
                elif patient.father_age_at_birth == "36-38":
                    sheet[f'W19'] = "yes" if patient.father_age_at_birth else 'no'
                elif patient.father_age_at_birth == "39-40":
                    sheet[f'Y19'] = "yes" if patient.father_age_at_birth else 'no'
                elif patient.father_age_at_birth == "40-42":
                    sheet[f'AZ19'] = "yes" if patient.father_age_at_birth else 'no'
                elif patient.father_age_at_birth == "43-45":
                    sheet[f'BB19'] = "yes" if patient.father_age_at_birth else 'no'
                elif patient.father_age_at_birth == "46-48":
                    sheet[f'DD19'] = "yes" if patient.father_age_at_birth else 'no'
                elif patient.father_age_at_birth == "49-50":
                    sheet[f'FF19'] = "yes" if patient.father_age_at_birth else 'no'

                sheet[f'G21'] = "yes" if patient.normal_motor_development else 'no'
                sheet[f'K21'] = "yes" if patient.hypotonia else 'no'
                sheet[f'M21'] = "yes" if patient.ataxia else 'no'

                sheet[f'G23'] = "yes" if patient.normal_cognitive_development else 'no'
                sheet[f'K23'] = "yes" if patient.learning_disability else 'no'
                sheet[f'N23'] = "yes" if patient.mental_disability else 'no'

                sheet[f'G25'] = "yes" if patient.normal_behavior else 'no'
                sheet[f'K25'] = "yes" if patient.hyperactive else 'no'
                sheet[f'N25'] = "yes" if patient.aggressive else 'no'
                sheet[f'Q25'] = "yes" if patient.aggressive_traits else 'no'
                sheet[f'U25'] = "yes" if patient.autistic else 'no'
                sheet[f'Y25'] = "yes" if patient.autistic_traits else 'no'
                sheet[f'AC25'] = "yes" if patient.obsessive else 'no'

                sheet[f'I27'] = patient.first_seizure_occurrence if patient.first_seizure_occurrence else 'no'
                sheet[f'X27'] = patient.seizure_duration if patient.seizure_duration else 'no'

                sheet[f'I28'] = f"yes" if patient.family_epilepsy else 'no'
                sheet[f'N28'] = patient.family_epilepsy_description if patient.family_epilepsy_description else 'no'
                sheet[f'AD28'] = patient.seizure_type if patient.seizure_type else 'no'

                if patient.focal_duration:
                    sheet[f'G30'] = f"yes" if patient.focal_duration else 'no'
                    sheet[f'J30'] = patient.focal_duration if patient.focal_duration else 'no'
                    sheet[f'N30'] = patient.focal_duration_description if patient.focal_duration_description else 'no'
                else:
                    sheet[f'G30'] = 'no'
                    sheet[f'J30'] = 'no'
                    sheet[f'N30'] = 'no'

                if patient.gtc_duration:
                    sheet[f'G31'] = f"yes" if patient.gtc_duration else 'no'
                    sheet[f'J31'] = patient.gtc_duration if patient.gtc_duration else 'no'
                    sheet[f'N31'] = patient.gtc_duration_description if patient.gtc_duration_description else 'no'
                else:
                    sheet[f'G31'] = 'no'
                    sheet[f'J31'] = 'no'
                    sheet[f'N31'] = 'no'

                if patient.tonic_duration:
                    sheet[f'G32'] = f"yes" if patient.tonic_duration else 'no'
                    sheet[f'J32'] = patient.tonic_duration if patient.tonic_duration else 'no'
                    sheet[f'N32'] = patient.tonic_duration_description if patient.tonic_duration_description else 'no'
                else:
                    sheet[f'G32'] = 'no'
                    sheet[f'J32'] = 'no'
                    sheet[f'N32'] = 'no'

                if patient.clonic_duration:
                    sheet[f'G33'] = f"yes" if patient.clonic_duration else 'no'
                    sheet[f'J33'] = patient.clonic_duration if patient.clonic_duration else 'no'
                    sheet[f'N33'] = patient.clonic_duration_description if patient.clonic_duration_description else 'no'
                else:
                    sheet[f'G33'] = 'no'
                    sheet[f'J33'] = 'no'
                    sheet[f'N33'] = 'no'

                if patient.tonic_clonic_duration:
                    sheet[f'G34'] = f"yes" if patient.tonic_clonic_duration else 'no'
                    sheet[f'J34'] = patient.tonic_clonic_duration if patient.tonic_clonic_duration else 'no'
                    sheet[f'N34'] = patient.tonic_clonic_duration_description if patient.tonic_clonic_duration_description else 'no'
                else:
                    sheet[f'G34'] = 'no'
                    sheet[f'J34'] = 'no'
                    sheet[f'N34'] = 'no'

                if patient.myoclonic_duration:
                    sheet[f'G35'] = f"yes" if patient.myoclonic_duration else 'no'
                    sheet[f'J35'] = patient.myoclonic_duration if patient.myoclonic_duration else 'no'
                    sheet[f'N35'] = patient.myoclonic_duration_description if patient.myoclonic_duration_description else 'no'
                else:
                    sheet[f'G35'] = 'no'
                    sheet[f'J35'] = 'no'
                    sheet[f'N35'] = 'no'

                if patient.absence_duration:
                    sheet[f'G36'] = f"yes" if patient.absence_duration else 'no'
                    sheet[f'J36'] = patient.absence_duration if patient.absence_duration else 'no'
                    sheet[f'N36'] = patient.absence_duration_description if patient.absence_duration_description else 'no'
                else:
                    sheet[f'G36'] = 'no'
                    sheet[f'J36'] = 'no'
                    sheet[f'N36'] = 'no'

                if patient.spasm_duration:
                    sheet[f'G37'] = f"yes" if patient.spasm_duration else 'no'
                    sheet[f'J37'] = patient.spasm_duration if patient.spasm_duration else 'no'
                    sheet[f'N37'] = patient.spasm_duration_description if patient.spasm_duration_description else 'no'
                else:
                    sheet[f'G37'] = 'no'
                    sheet[f'J37'] = 'no'
                    sheet[f'N37'] = 'no'

                if patient.s_febrile_seizure_duration:
                    sheet[f'G38'] = f"yes" if patient.s_febrile_seizure_duration else 'no'
                    sheet[f'J38'] = patient.s_febrile_seizure_duration if patient.s_febrile_seizure_duration else 'no'
                    sheet[f'N38'] = patient.s_febrile_seizure_duration_description if patient.s_febrile_seizure_duration_description else 'no'
                else:
                    sheet[f'G38'] = 'no'
                    sheet[f'J38'] = 'no'
                    sheet[f'N38'] = 'no'

                if patient.c_febrile_seizure_duration:
                    sheet[f'G39'] = f"yes" if patient.c_febrile_seizure_duration else 'no'
                    sheet[f'J39'] = patient.c_febrile_seizure_duration if patient.c_febrile_seizure_duration else 'no'
                    sheet[f'N39'] = patient.c_febrile_seizure_duration_description if patient.c_febrile_seizure_duration_description else 'no'
                else:
                    sheet[f'G39'] = 'no'
                    sheet[f'J39'] = 'no'
                    sheet[f'N39'] = 'no'

                if patient.neonatal_seizure_duration:
                    sheet[f'AA30'] = f"yes" if patient.neonatal_seizure_duration else 'no'
                    sheet[f'AC30'] = patient.neonatal_seizure_duration if patient.neonatal_seizure_duration else 'no'
                    sheet[f'AG30'] = patient.neonatal_seizure_duration_description if patient.neonatal_seizure_duration_description else 'no'
                else:
                    sheet[f'AA30'] = 'no'
                    sheet[f'AC30'] = 'no'
                    sheet[f'AG30'] = 'no'

                if patient.dependent_epilesy_duration:
                    sheet[f'AA31'] = f"yes" if patient.dependent_epilesy_duration else 'no'
                    sheet[f'AC31'] = patient.dependent_epilesy_duration if patient.dependent_epilesy_duration else 'no'
                    sheet[f'AG31'] = patient.dependent_epilesy_description if patient.dependent_epilesy_description else 'no'
                else:
                    sheet[f'AA31'] = 'no'
                    sheet[f'AC31'] = 'no'
                    sheet[f'AG31'] = 'no'

                if patient.Familial_infantile_duration:
                    sheet[f'AA32'] = f"yes" if patient.Familial_infantile_duration else 'no'
                    sheet[f'AC32'] = patient.Familial_infantile_duration if patient.Familial_infantile_duration else 'no'
                    sheet[f'AG32'] = patient.Familial_infantile_description if patient.Familial_infantile_description else 'no'
                else:
                    sheet[f'AA32'] = 'no'
                    sheet[f'AC32'] = 'no'
                    sheet[f'AG32'] = 'no'

                if patient.dravet_syndrom_duration:
                    sheet[f'AA33'] = f"yes" if patient.dravet_syndrom_duration else 'no'
                    sheet[f'AC33'] = patient.dravet_syndrom_duration if patient.dravet_syndrom_duration else 'no'
                    sheet[f'AG33'] = patient.dravet_syndrom_description if patient.dravet_syndrom_description else 'no'
                else:
                    sheet[f'AA33'] = 'no'
                    sheet[f'AC33'] = 'no'
                    sheet[f'AG33'] = 'no'

                if patient.glut1_deficiency_duration:
                    sheet[f'AA34'] = f"yes" if patient.glut1_deficiency_duration else 'no'
                    sheet[f'AC34'] = patient.glut1_deficiency_duration if patient.glut1_deficiency_duration else 'no'
                    sheet[f'AG34'] = patient.glut1_deficiency_description if patient.glut1_deficiency_description else 'no'
                else:
                    sheet[f'AA34'] = 'no'
                    sheet[f'AC34'] = 'no'
                    sheet[f'AG34'] = 'no'

                if patient.fcd_typ_duration:
                    sheet[f'AA35'] = f"yes" if patient.fcd_typ_duration else 'no'
                    sheet[f'AC35'] = patient.fcd_typ_duration if patient.fcd_typ_duration else 'no'
                    sheet[f'AG35'] = patient.fcd_typ_description if patient.fcd_typ_description else 'no'
                else:
                    sheet[f'AA35'] = 'no'
                    sheet[f'AC35'] = 'no'
                    sheet[f'AG35'] = 'no'

                if patient.epileptic_duration:
                    sheet[f'AA36'] = f"yes" if patient.epileptic_duration else 'no'
                    sheet[f'AC36'] = patient.epileptic_duration if patient.epileptic_duration else 'no'
                    sheet[f'AG36'] = patient.epileptic_description if patient.epileptic_description else 'no'
                else:
                    sheet[f'AA36'] = 'no'
                    sheet[f'AC36'] = 'no'
                    sheet[f'AG36'] = 'no'

                if patient.eme_duration:
                    sheet[f'AA37'] = f"yes" if patient.eme_duration else 'no'
                    sheet[f'AC37'] = patient.eme_duration if patient.eme_duration else 'no'
                    sheet[f'AG37'] = patient.eme_duration_description if patient.eme_duration_description else 'no'
                else:
                    sheet[f'AA37'] = 'no'
                    sheet[f'AC37'] = 'no'
                    sheet[f'AG37'] = 'no'

                if patient.eimfs_duration:
                    sheet[f'AA38'] = f"yes" if patient.eimfs_duration else 'no'
                    sheet[f'AC38'] = patient.eimfs_duration if patient.eimfs_duration else 'no'
                    sheet[f'AG38'] = patient.eimfs_duration_description if patient.eimfs_duration_description else 'no'
                else:
                    sheet[f'AA38'] = 'no'
                    sheet[f'AC38'] = 'no'
                    sheet[f'AG38'] = 'no'

                if patient.eoee_duration:
                    sheet[f'H41'] = f"yes" if patient.eoee_duration else 'no'
                    sheet[f'J41'] = patient.eoee_duration if patient.eoee_duration else 'no'
                    sheet[f'N41'] = patient.eoee_duration_description if patient.eoee_duration_description else 'no'
                else:
                    sheet[f'H41'] = 'no'
                    sheet[f'J41'] = 'no'
                    sheet[f'N41'] = 'no'

                if patient.infantiles_duration:
                    sheet[f'H42'] = f"yes" if patient.infantiles_duration else 'no'
                    sheet[f'J42'] = patient.infantiles_duration if patient.infantiles_duration else 'no'
                    sheet[f'N42'] = patient.infantiles_duration_description if patient.infantiles_duration_description else 'no'
                else:
                    sheet[f'H42'] = 'no'
                    sheet[f'J42'] = 'no'
                    sheet[f'N42'] = 'no'

                if patient.sw_duration:
                    sheet[f'H43'] = f"yes" if patient.sw_duration else 'no'
                    sheet[f'J43'] = patient.sw_duration if patient.sw_duration else 'no'
                    sheet[f'N43'] = patient.sw_duration_description if patient.sw_duration_description else 'no'
                else:
                    sheet[f'H43'] = 'no'
                    sheet[f'J43'] = 'no'
                    sheet[f'N43'] = 'no'

                if patient.so_duration:
                    sheet[f'H44'] = f"yes" if patient.so_duration else 'no'
                    sheet[f'J44'] = patient.so_duration if patient.so_duration else 'no'
                    sheet[f'N44'] = patient.so_duration_description if patient.so_duration_description else 'no'
                else:
                    sheet[f'H44'] = 'no'
                    sheet[f'J44'] = 'no'
                    sheet[f'N44'] = 'no'

                if patient.sd_duration:
                    sheet[f'H45'] = f"yes" if patient.sd_duration else 'no'
                    sheet[f'J45'] = patient.sd_duration if patient.sd_duration else 'no'
                    sheet[f'N45'] = patient.sd_duration_description if patient.sd_duration_description else 'no'
                else:
                    sheet[f'H45'] = 'no'
                    sheet[f'J45'] = 'no'
                    sheet[f'N45'] = 'no'

                if patient.lgs_duration:
                    sheet[f'H46'] = f"yes" if patient.lgs_duration else 'no'
                    sheet[f'J46'] = patient.lgs_duration if patient.lgs_duration else 'no'
                    sheet[f'N46'] = patient.lgs_duration_description if patient.lgs_duration_description else 'no'
                else:
                    sheet[f'H46'] = 'no'
                    sheet[f'J46'] = 'no'
                    sheet[f'N46'] = 'no'

                if patient.emas_duration:
                    sheet[f'H47'] = f"yes" if patient.emas_duration else 'no'
                    sheet[f'J47'] = patient.emas_duration if patient.emas_duration else 'no'
                    sheet[f'N47'] = patient.emas_duration_description if patient.emas_duration_description else 'no'
                else:
                    sheet[f'H47'] = 'no'
                    sheet[f'J47'] = 'no'
                    sheet[f'N47'] = 'no'

                if patient.lks_duration:
                    sheet[f'H48'] = f"yes" if patient.lks_duration else 'no'
                    sheet[f'J48'] = patient.lks_duration if patient.lks_duration else 'no'
                    sheet[f'N48'] = patient.lks_duration_description if patient.lks_duration_description else 'no'
                else:
                    sheet[f'H48'] = 'no'
                    sheet[f'J48'] = 'no'
                    sheet[f'N48'] = 'no'

                if patient.gge_duration:
                    sheet[f'H49'] = f"yes" if patient.gge_duration else 'no'
                    sheet[f'J49'] = patient.gge_duration if patient.gge_duration else 'no'
                    sheet[f'N49'] = patient.gge_duration_description if patient.gge_duration_description else 'no'
                else:
                    sheet[f'H49'] = 'no'
                    sheet[f'J49'] = 'no'
                    sheet[f'N49'] = 'no'

                if patient.cae_duration:
                    sheet[f'AA41'] = f"yes" if patient.cae_duration else 'no'
                    sheet[f'AC41'] = patient.cae_duration if patient.cae_duration else 'no'
                    sheet[f'AG41'] = patient.cae_duration_description if patient.cae_duration_description else 'no'
                else:
                    sheet[f'AA41'] = 'no'
                    sheet[f'AC41'] = 'no'
                    sheet[f'AG41'] = 'no'

                if patient.jae_duration:
                    sheet[f'AA42'] = f"yes" if patient.jae_duration else 'no'
                    sheet[f'AC42'] = patient.jae_duration if patient.jae_duration else 'no'
                    sheet[f'AG42'] = patient.jae_duration_description if patient.jae_duration_description else 'no'
                else:
                    sheet[f'AA42'] = 'no'
                    sheet[f'AC42'] = 'no'
                    sheet[f'AG42'] = 'no'

                if patient.jme_duration:
                    sheet[f'AA43'] = f"yes" if patient.jme_duration else 'no'
                    sheet[f'AC43'] = patient.jme_duration if patient.jme_duration else 'no'
                    sheet[f'AG43'] = patient.jme_duration_description if patient.jme_duration_description else 'no'
                else:
                    sheet[f'AA43'] = 'no'
                    sheet[f'AC43'] = 'no'
                    sheet[f'AG43'] = 'no'

                if patient.tle_duration:
                    sheet[f'AA44'] = f"yes" if patient.tle_duration else 'no'
                    sheet[f'AC44'] = patient.tle_duration if patient.tle_duration else 'no'
                    sheet[f'AG44'] = patient.tle_duration_description if patient.tle_duration_description else 'no'
                else:
                    sheet[f'AA44'] = 'no'
                    sheet[f'AC44'] = 'no'
                    sheet[f'AG44'] = 'no'

                if patient.ge_duration:
                    sheet[f'AA45'] = f"yes" if patient.ge_duration else 'no'
                    sheet[f'AC45'] = patient.ge_duration if patient.ge_duration else 'no'
                    sheet[f'AG45'] = patient.ge_duration_description if patient.ge_duration_description else 'no'
                else:
                    sheet[f'AA45'] = 'no'
                    sheet[f'AC45'] = 'no'
                    sheet[f'AG45'] = 'no'

                if patient.sws_duration:
                    sheet[f'AA46'] = f"yes" if patient.sws_duration else 'no'
                    sheet[f'AC46'] = patient.sws_duration if patient.sws_duration else 'no'
                    sheet[f'AG46'] = patient.sws_duration_description if patient.sws_duration_description else 'no'
                else:
                    sheet[f'AA46'] = 'no'
                    sheet[f'AC46'] = 'no'
                    sheet[f'AG46'] = 'no'

                if patient.deeswas_duration:
                    sheet[f'AA47'] = f"yes" if patient.deeswas_duration else 'no'
                    sheet[f'AC47'] = patient.deeswas_duration if patient.deeswas_duration else 'no'
                    sheet[f'AG47'] = patient.deeswas_duration_description if patient.deeswas_duration_description else 'no'
                else:
                    sheet[f'AA47'] = 'no'
                    sheet[f'AC47'] = 'no'
                    sheet[f'AG47'] = 'no'

                if patient.eesws_duration:
                    sheet[f'AA48'] = f"yes" if patient.eesws_duration else 'no'
                    sheet[f'AC48'] = patient.eesws_duration if patient.eesws_duration else 'no'
                    sheet[f'AG48'] = patient.eeesws_duration_description if patient.eeesws_duration_description else 'no'
                else:
                    sheet[f'AA48'] = 'no'
                    sheet[f'AC48'] = 'no'
                    sheet[f'AG48'] = 'no'

                if patient.nm_duration:
                    sheet[f'AA49'] = f"yes" if patient.nm_duration else 'no'
                    sheet[f'AC49'] = patient.nm_duration if patient.nm_duration else 'no'
                    sheet[f'AG49'] = patient.nm_duration_description if patient.nm_duration_description else 'no'
                else:
                    sheet[f'AA49'] = 'no'
                    sheet[f'AC49'] = 'no'
                    sheet[f'AG49'] = 'no'

                if patient.gms_duration:
                    sheet[f'H51'] = f"yes" if patient.gms_duration else 'no'
                    sheet[f'J51'] = patient.gms_duration if patient.gms_duration else 'no'
                    sheet[f'N51'] = patient.gms_duration_description if patient.gms_duration_description else 'no'
                else:
                    sheet[f'H51'] = 'no'
                    sheet[f'J51'] = 'no'
                    sheet[f'N51'] = 'no'

                if patient.nfle_duration:
                    sheet[f'H52'] = f"yes" if patient.nfle_duration else 'no'
                    sheet[f'J52'] = patient.nfle_duration if patient.nfle_duration else 'no'
                    sheet[f'N52'] = patient.nfle_duration_description if patient.nfle_duration_description else 'no'
                else:
                    sheet[f'H52'] = 'no'
                    sheet[f'J52'] = 'no'
                    sheet[f'N52'] = 'no'

                if patient.mae_duration:
                    sheet[f'H53'] = f"yes" if patient.mae_duration else 'no'
                    sheet[f'J53'] = patient.mae_duration if patient.mae_duration else 'no'
                    sheet[f'N53'] = patient.mae_duration_description if patient.mae_duration_description else 'no'
                else:
                    sheet[f'H53'] = 'no'
                    sheet[f'J53'] = 'no'
                    sheet[f'N53'] = 'no'

                if patient.coee_duration:
                    sheet[f'H54'] = f"yes" if patient.coee_duration else 'no'
                    sheet[f'J54'] = patient.coee_duration if patient.coee_duration else 'no'
                    sheet[f'N54'] = patient.coee_duration_description if patient.coee_duration_description else 'no'
                else:
                    sheet[f'H54'] = 'no'
                    sheet[f'J54'] = 'no'
                    sheet[f'N54'] = 'no'

                if patient.ftle_duration:
                    sheet[f'H55'] = f"yes" if patient.ftle_duration else 'no'
                    sheet[f'J55'] = patient.ftle_duration if patient.ftle_duration else 'no'
                    sheet[f'N55'] = patient.ftle_duration_description if patient.ftle_duration_description else 'no'
                else:
                    sheet[f'H55'] = 'no'
                    sheet[f'J55'] = 'no'
                    sheet[f'N55'] = 'no'

                if patient.bfis_duration:
                    sheet[f'H56'] = f"yes" if patient.bfis_duration else 'no'
                    sheet[f'J56'] = patient.bfis_duration if patient.bfis_duration else 'no'
                    sheet[f'N56'] = patient.bfis_duration_description if patient.bfis_duration_description else 'no'
                else:
                    sheet[f'H56'] = 'no'
                    sheet[f'J56'] = 'no'
                    sheet[f'N56'] = 'no'

                if patient.bfns_duration:
                    sheet[f'H57'] = f"yes" if patient.bfns_duration else 'no'
                    sheet[f'J57'] = patient.bfns_duration if patient.bfns_duration else 'no'
                    sheet[f'N57'] = patient.bfns_duration_description if patient.bfns_duration_description else 'no'
                else:
                    sheet[f'H57'] = 'no'
                    sheet[f'J57'] = 'no'
                    sheet[f'N57'] = 'no'

                if patient.gepd_duration:
                    sheet[f'H58'] = f"yes" if patient.gepd_duration else 'no'
                    sheet[f'J58'] = patient.gepd_duration if patient.gepd_duration else 'no'
                    sheet[f'N58'] = patient.gepd_duration_description if patient.gepd_duration_description else 'no'
                else:
                    sheet[f'H58'] = 'no'
                    sheet[f'J58'] = 'no'
                    sheet[f'N58'] = 'no'

                if patient.dre_duration:
                    sheet[f'H59'] = f"yes" if patient.dre_duration else 'no'
                    sheet[f'J59'] = patient.dre_duration if patient.dre_duration else 'no'
                    sheet[f'N59'] = patient.dre_duration_description if patient.dre_duration_description else 'no'
                else:
                    sheet[f'H59'] = 'no'
                    sheet[f'J59'] = 'no'
                    sheet[f'N59'] = 'no'


                sheet[f'G61'] = f"yes" if patient.progressive_microcephaly else 'no'
                sheet[f'G62'] = f"yes" if patient.congenital_microcephaly else 'no'
                sheet[f'G63'] = f"yes" if patient.focal_brain_malformation else 'no'
                sheet[f'G64'] = f"yes" if patient.multifocal_brain_malformation else 'no'
                sheet[f'G65'] = f"yes" if patient.polimicrogria else 'no'
                sheet[f'G66'] = f"yes" if patient.optic_nerve_atrophy else 'no'
                sheet[f'G67'] = f"yes" if patient.holoprosencephaly else 'no'
                sheet[f'G68'] = f"yes" if patient.heterotopia else 'no'

                #MRI 2
                sheet[f'N61'] = f"yes" if patient.tuberous_sclerosis else 'no'
                sheet[f'N62'] = f"yes" if patient.hypothalamic_hamartoma else 'no'
                sheet[f'N63'] = f"yes" if patient.leucodystrophy else 'no'
                sheet[f'N64'] = f"yes" if patient.lissencephaly else 'no'
                sheet[f'N65'] = f"yes" if patient.intracranial_hemorrhage else 'no'
                sheet[f'N66'] = f"yes" if patient.cerebral_venous_sinus_thrombosis else 'no'
                sheet[f'N67'] = f"yes" if patient.atrophy else 'no'
                sheet[f'N68'] = f"yes" if patient.hypoplasia_corpus_callosum else 'no'

                #MRI3
                sheet[f'X61'] = f"yes" if patient.corpus_callosum_atrophy else 'no'
                sheet[f'X62'] = f"yes" if patient.ventriculomegaly else 'no'
                sheet[f'X63'] = f"yes" if patient.white_matter_changes else 'no'
                sheet[f'X64'] = f"yes" if patient.cerebral_atrophy else 'no'
                sheet[f'X65'] = f"yes" if patient.cerebellar_atrophy else 'no'
                sheet[f'X66'] = f"yes" if patient.basal_ganga else 'no'
                sheet[f'X67'] = f"yes" if patient.hypoxic_ischemic_barin else 'no'
                sheet[f'X68'] = f"yes" if patient.hydrocephalus else 'no'
                sheet[f'AI61'] = f"yes" if patient.development_delay else 'no'
                sheet[f'AI62'] = f"yes" if patient.development_delay_and_epilepsy else 'no'
                sheet[f'AI63'] = f"yes" if patient.epilepsy_only else 'no'

                #eeg
                sheet[f'AA70'] = f"yes" if patient.fed else 'no'
                sheet[f'AA71'] = f"yes" if patient.g else 'no'
                sheet[f'AA72'] = f"yes" if patient.fed_g else 'no'
                sheet[f'AA73'] = f"yes" if patient.swa else 'no'
                sheet[f'AA74'] = f"yes" if patient.bs else 'no'
                sheet[f'AA75'] = f"yes" if patient.normal else 'no'


                #FEVER
                sheet[f'G71'] = f"yes" if patient.afebrile_infections else 'no'
                sheet[f'G72'] = f"yes" if patient.vaccinations else 'no'
                sheet[f'G73'] = f"yes" if patient.emotional_stress else 'no'
                sheet[f'G74'] = f"yes" if patient.hot_bathing else 'no'
                sheet[f'G75'] = f"yes" if patient.motor_activity else 'no'
                sheet[f'G76'] = f"yes" if patient.photostimulation else 'no'
                sheet[f'G77'] = f"yes" if patient.hyperventilation else 'no'

                #ASM
                sheet[f'E79'] = f"yes" if patient.br_dose else 'no'
                sheet[f'H79'] = patient.br_dose if patient.br_dose else 'no'
                sheet[f'K79'] = patient.br_description if patient.br_description else 'no'

                sheet[f'E80'] = f"yes" if patient.cbz_dose else 'no'
                sheet[f'H80'] = patient.cbz_dose if patient.cbz_dose else 'no'
                sheet[f'K80'] = patient.cbz_description if patient.cbz_description else 'no'

                sheet[f'E81'] = f"yes" if patient.clb_dose else 'no'
                sheet[f'H81'] = patient.clb_dose if patient.clb_dose else 'no'
                sheet[f'K81'] = patient.clb_description if patient.clb_description else 'no'

                sheet[f'E82'] = f"yes" if patient.czp_dose else 'no'
                sheet[f'H82'] = patient.czp_dose if patient.czp_dose else 'no'
                sheet[f'K82'] = patient.czp_description if patient.czp_description else 'no'

                sheet[f'E83'] = f"yes" if patient.esm_dose else 'no'
                sheet[f'H83'] = patient.esm_dose if patient.esm_dose else 'no'
                sheet[f'K83'] = patient.esm_description if patient.esm_description else 'no'

                sheet[f'E84'] = f"yes" if patient.lzp_dose else 'no'
                sheet[f'H84'] = patient.lzp_dose if patient.lzp_dose else 'no'
                sheet[f'K84'] = patient.lzp_description if patient.lzp_description else 'no'

                sheet[f'E85'] = f"yes" if patient.lcm_dose else 'no'
                sheet[f'H85'] = patient.lcm_dose if patient.lcm_dose else 'no'
                sheet[f'K85'] = patient.lcm_description if patient.lcm_description else 'no'

                sheet[f'E86'] = f"yes" if patient.lev_dose else 'no'
                sheet[f'H86'] = patient.lev_dose if patient.lev_dose else 'no'
                sheet[f'K86'] = patient.lev_description if patient.lev_description else 'no'

                sheet[f'E87'] = f"yes" if patient.ltg_dose else 'no'
                sheet[f'H87'] = patient.ltg_dose if patient.ltg_dose else 'no'
                sheet[f'K87'] = patient.ltg_description if patient.ltg_description else 'no'

                sheet[f'E88'] = f"yes" if patient.lzp_dose else 'no'
                sheet[f'H88'] = patient.lzp_dose if patient.lzp_dose else 'no'
                sheet[f'K88'] = patient.lzp_description if patient.lzp_description else 'no'

                sheet[f'E89'] = f"yes" if patient.vgb_dose else 'no'
                sheet[f'H89'] = patient.vgb_dose if patient.vgb_dose else 'no'
                sheet[f'K89'] = patient.vgb_description if patient.vgb_description else 'no'

                sheet[f'E90'] = f"yes" if patient.vpa_dose else 'no'
                sheet[f'H90'] = patient.vpa_dose if patient.vpa_dose else 'no'
                sheet[f'K90'] = patient.vpa_description if patient.vpa_description else 'no'

                sheet[f'E91'] = f"yes" if patient.zns_dose else 'no'
                sheet[f'H91'] = patient.zns_dose if patient.zns_dose else 'no'
                sheet[f'K91'] = patient.zns_description if patient.zns_description else 'no'

                sheet[f'U79'] = f"yes" if patient.nzp_dose else 'no'
                sheet[f'W79'] = patient.nzp_dose if patient.nzp_dose else 'no'
                sheet[f'Z79'] = patient.nzp_description if patient.nzp_description else 'no'

                sheet[f'U80'] = f"yes" if patient.oxc_dose else 'no'
                sheet[f'W80'] = patient.oxc_dose if patient.oxc_dose else 'no'
                sheet[f'Z80'] = patient.oxc_description if patient.oxc_description else 'no'

                sheet[f'U81'] = f"yes" if patient.pb_dose else 'no'
                sheet[f'W81'] = patient.pb_dose if patient.pb_dose else 'no'
                sheet[f'Z81'] = patient.pb_description if patient.pb_description else 'no'

                sheet[f'U82'] = f"yes" if patient.per_dose else 'no'
                sheet[f'W82'] = patient.per_dose if patient.per_dose else 'no'
                sheet[f'Z82'] = patient.per_description if patient.per_description else 'no'

                sheet[f'U83'] = f"yes" if patient.pgb_dose else 'no'
                sheet[f'W83'] = patient.pgb_dose if patient.pgb_dose else 'no'
                sheet[f'Z83'] = patient.pgb_description if patient.pgb_description else 'no'

                sheet[f'U84'] = f"yes" if patient.pht_dose else 'no'
                sheet[f'W84'] = patient.pht_dose if patient.pht_dose else 'no'
                sheet[f'Z84'] = patient.pht_description if patient.pht_description else 'no'

                sheet[f'U85'] = f"yes" if patient.rfn_dose else 'no'
                sheet[f'W85'] = patient.rfn_dose if patient.rfn_dose else 'no'
                sheet[f'Z85'] = patient.rfn_description if patient.rfn_description else 'no'

                sheet[f'U86'] = f"yes" if patient.stm_dose else 'no'
                sheet[f'W86'] = patient.stm_dose if patient.stm_dose else 'no'
                sheet[f'Z86'] = patient.stm_description if patient.stm_description else 'no'

                sheet[f'U87'] = f"yes" if patient.stp_dose else 'no'
                sheet[f'W87'] = patient.stp_dose if patient.stp_dose else 'no'
                sheet[f'Z87'] = patient.stp_description if patient.stp_description else 'no'

                sheet[f'U88'] = f"yes" if patient.tpm_dose else 'no'
                sheet[f'W88'] = patient.tpm_dose if patient.tpm_dose else 'no'
                sheet[f'Z88'] = patient.tpm_description if patient.tpm_description else 'no'

                sheet[f'U89'] = f"yes" if patient.esm_dose else 'no'
                sheet[f'W89'] = patient.esm_dose if patient.esm_dose else 'no'
                sheet[f'Z89'] = patient.esm_description if patient.esm_description else 'no'

                sheet[f'U90'] = f"yes" if patient.pgb_dose else 'no'
                sheet[f'W90'] = patient.pgb_dose if patient.pgb_dose else 'no'
                sheet[f'Z90'] = patient.pgb_description if patient.pgb_description else 'no'

                sheet[f'AH80'] = f"yes" if patient.nausea else 'no'
                sheet[f'AH81'] = f"yes" if patient.vomiting else 'no'
                sheet[f'AH82'] = f"yes" if patient.rash else 'no'
                sheet[f'AH83'] = f"yes" if patient.edema else 'no'
                sheet[f'AH84'] = f"yes" if patient.constipation else 'no'
                sheet[f'AH85'] = f"yes" if patient.diarrhea else 'no'
                sheet[f'AH86'] = f"yes" if patient.anorexia else 'no'
                sheet[f'AH87'] = f"yes" if patient.stomach_pain else 'no'
                sheet[f'AH88'] = f"yes" if patient.hematological else 'no'
                sheet[f'AH89'] = f"yes" if patient.obesity else 'no'

                sheet['K92'] = f"yes" if patient.response_50_74_2 else 'no'
                sheet['Q92'] = f"yes" if patient.response_75_99_2 else 'no'
                sheet['W92'] = f"yes" if patient.response_100_2 else 'no'
                sheet['AC92'] = f"yes" if patient.non_response_2 else 'no'
                sheet['AI92'] = f"yes" if patient.aggravation_2 else 'no'

                sheet[f'E95'] = f"yes" if patient.methyl_prednisolone_dose else 'no'
                sheet[f'H95'] = patient.methyl_prednisolone_dose if patient.methyl_prednisolone_dose else 'no'
                sheet[f'K95'] = patient.methyl_prednisolone_description if patient.methyl_prednisolone_description else 'no'
                sheet[f'U95'] = f"yes" if patient.wes else 'no'
                sheet[f'W95'] = patient.pathogenic if patient.pathogenic else 'no'
                sheet[f'Z95'] = patient.like_pathogenic if patient.like_pathogenic else 'no'
                sheet[f'AE95'] = patient.vus if patient.vus else 'no'


                sheet[f'E96'] = f"yes" if patient.prednisolone_dose else 'no'
                sheet[f'H96'] = patient.prednisolone_dose if patient.prednisolone_dose else 'no'
                sheet[f'K96'] = patient.prednisolone_description if patient.prednisolone_description else 'no'

                sheet[f'E97'] = f"yes" if patient.dexamethasone_dose else 'no'
                sheet[f'H97'] = patient.dexamethasone_dose if patient.dexamethasone_dose else 'no'
                sheet[f'K97'] = patient.dexamethasone_description if patient.dexamethasone_description else 'no'

                sheet[f'E98'] = f"yes" if patient.acth_dose else 'no'
                sheet[f'H98'] = patient.acth_dose if patient.acth_dose else 'no'
                sheet[f'K98'] = patient.acth_description if patient.acth_description else 'no'

                sheet['E99'] = f"yes" if patient.hydrocortisone_dose else 'no'
                sheet['H99'] = patient.hydrocortisone_dose if patient.hydrocortisone_dose else 'no'
                sheet['K99'] = patient.hydrocortisone_description if patient.hydrocortisone_description else 'no'

                sheet['K100'] = f"yes" if patient.response_50_74 else 'no'
                sheet['Q100'] = f"yes" if patient.response_75_99 else 'no'
                sheet['W100'] = f"yes" if patient.response_100 else 'no'
                sheet['AC100'] = f"yes" if patient.non_response else 'no'
                sheet['AI100'] = f"yes" if patient.aggravation else 'no'

                if patient.other_medications_triggered_attack:
                    sheet['Z102'] = f"yes" if patient.other_medications_triggered_attack else 'no'
                    sheet[f'AB102'] = patient.other_medications_description if patient.other_medications_description else 'no'

                if patient.medication_missed:
                    sheet['J102'] = f"yes" if patient.medication_missed else 'no'
                    sheet[f'M102'] = patient.medication_missed_description if patient.medication_missed_description else 'no'

                sheet['E103'] = f"yes" if patient.farmacoresistant else 'no'
                sheet['I103'] = f"yes" if patient.change_of_2_aep else 'no'
                sheet['M103'] = f"yes" if patient.change_of_more_than_2_aep else 'no'
                sheet['R103'] = f"yes" if patient.monotherapy else 'no'
                sheet['V103'] = f"yes" if patient.duotherapy else 'no'
                sheet['Z103'] = f"yes" if patient.polytherapy else 'no'

                sheet['E104'] = patient.nsg if patient.nsg else 'no'
                sheet['E105'] = patient.audiogram if patient.audiogram else 'no'
                sheet['E106'] = patient.ophthalmologist if patient.ophthalmologist else 'no'
                sheet['E107'] = patient.genetic if patient.genetic else 'no'
                sheet['E108'] = patient.recommendations if patient.recommendations else 'no'
                sheet['E109'] = patient.clinical_diagnosis if patient.clinical_diagnosis else 'no'
                sheet['E110'] = patient.notes if patient.notes else 'no'

            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename=patient_{patient.full_name}.xlsx'
            workbook.save(response)
            return response

        except Exception as e:
            return HttpResponse(f"Error generating Excel: {str(e)}", status=500)