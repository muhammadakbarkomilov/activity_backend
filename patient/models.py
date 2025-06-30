from lib2to3.pgen2.tokenize import blank_re

from django.db import models

class PatientData(models.Model):
    # Personal Information
    reg_no = models.TextField(max_length=100, null=False, blank=False)
    history_t = models.TextField(blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    date_of_examination = models.DateField(blank=True, null=True)

    # Family History
    consanguineous_marriage = models.BooleanField(blank=True, null=True)
    consanguineous_marriage_description = models.TextField(blank=True, null=True)
    hereditary_diseases = models.BooleanField(blank=True, null=True)
    hereditary_diseases_description = models.TextField(blank=True, null=True)

    # Pregnancy Information
    gestation_period = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        choices=[
            ('28-29', '28-29 weeks'),
            ('30-31', '30-31 weeks'),
            ('32-33', '32-33 weeks'),
            ('34-35', '34-35 weeks'),
            ('36-37', '36-37 weeks'),
            ('38-39', '38-39 weeks'),
            ('40-41', '40-41 weeks'),
        ]
    )
    pregnancy_number = models.IntegerField(null=True, blank=True)
    childbirth_number = models.IntegerField(null=True, blank=True)

    # Labor Pathology
    rapid_labor = models.BooleanField(blank=True, null=True)
    protracted_labor = models.BooleanField(blank=True, null=True)
    weakness_occupation = models.BooleanField(blank=True, null=True)
    placental_abruption = models.BooleanField(blank=True, null=True)
    increased_blood_pressure = models.BooleanField(blank=True, null=True)
    post_term = models.BooleanField(blank=True, null=True)
    preterm = models.BooleanField(blank=True, null=True)

    # Pregnancy Complications
    first_half_medication = models.BooleanField(blank=True, null=True)
    first_half_medication_description = models.TextField(blank=True, null=True)
    first_half_toxicosis = models.BooleanField(blank=True, null=True)
    first_half_threatened_miscarriage = models.BooleanField(blank=True, null=True)
    first_half_arv = models.BooleanField(blank=True, null=True)
    first_half_stress = models.BooleanField(blank=True, null=True)
    first_half_anemia = models.BooleanField(blank=True, null=True)
    first_half_rh_incompatibility = models.BooleanField(blank=True, null=True)

    second_half_medication = models.BooleanField(blank=True, null=True)
    second_half_medication_description = models.TextField(blank=True, null=True)
    second_half_toxicosis = models.BooleanField(blank=True, null=True)
    second_half_threatened_miscarriage = models.BooleanField(blank=True, null=True)
    second_half_arv = models.BooleanField(blank=True, null=True)
    second_half_stress = models.BooleanField(blank=True, null=True)
    second_half_anemia = models.BooleanField(blank=True, null=True)
    second_half_rh_incompatibility = models.BooleanField(blank=True, null=True)

    # Parent Ages
    mother_age_at_birth = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        choices=[
            ('15-17', '15-17 years'),
            ('18-20', '18-20 years'),
            ('21-23', '21-23 years'),
            ('24-26', '24-26 years'),
            ('27-29', '27-29 years'),
            ('30-32', '30-32 years'),
            ('33-35', '33-35 years'),
            ('36-38', '36-38 years'),
            ('39-40', '39-40 years'),
            ('40-42', '40-42 years'),
            ('43-45', '43-45 years'),
            ('46-48', '46-48 years'),
            ('49-50', '49-50 years'),
        ]
    )

    father_age_at_birth = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        choices=[
            ('15-17', '15-17 years'),
            ('18-20', '18-20 years'),
            ('21-23', '21-23 years'),
            ('24-26', '24-26 years'),
            ('27-29', '27-29 years'),
            ('30-32', '30-32 years'),
            ('33-35', '33-35 years'),
            ('36-38', '36-38 years'),
            ('39-40', '39-40 years'),
            ('40-42', '40-42 years'),
            ('43-45', '43-45 years'),
            ('46-48', '46-48 years'),
            ('49-50', '49-50 years'),
        ]
    )

    # Child Development
    normal_motor_development = models.BooleanField(blank=True, null=True)
    hypotonia = models.BooleanField(blank=True, null=True)
    ataxia = models.BooleanField(blank=True, null=True)

    normal_cognitive_development = models.BooleanField(blank=True, null=True)
    learning_disability = models.BooleanField(blank=True, null=True)
    mental_disability = models.BooleanField(blank=True, null=True)

    normal_behavior = models.BooleanField(blank=True, null=True)
    hyperactive = models.BooleanField(blank=True, null=True)
    aggressive = models.BooleanField(blank=True, null=True)
    aggressive_traits = models.BooleanField(blank=True, null=True)
    autistic = models.BooleanField(blank=True, null=True)
    autistic_traits = models.BooleanField(blank=True, null=True)
    obsessive = models.BooleanField(blank=True, null=True)

    # Epilepsy History
    first_seizure_occurrence = models.CharField(max_length=255, blank=True, null=True)
    seizure_duration = models.CharField(max_length=255, blank=True, null=True)
    family_epilepsy = models.BooleanField(blank=True, null=True)
    family_epilepsy_description = models.TextField(blank=True, null=True)
    seizure_type = models.CharField(max_length=255, blank=True, null=True)

    # Seizure Information
    focal_duration = models.TextField(blank=True, null=True)
    focal_duration_description = models.TextField(blank=True, null=True)
    gtc_duration = models.TextField(blank=True, null=True)
    gtc_duration_description = models.TextField(blank=True, null=True)
    tonic_duration = models.TextField(blank=True, null=True)
    tonic_duration_description = models.TextField(blank=True, null=True)
    clonic_duration = models.TextField(blank=True, null=True)
    clonic_duration_description = models.TextField(blank=True, null=True)
    tonic_clonic_duration = models.TextField(blank=True, null=True)
    tonic_clonic_duration_description = models.TextField(blank=True, null=True)
    myoclonic_duration = models.TextField(blank=True, null=True)
    myoclonic_duration_description = models.TextField(blank=True, null=True)
    absence_duration = models.TextField(blank=True, null=True)
    absence_duration_description = models.TextField(blank=True, null=True)
    spasm_duration = models.TextField(blank=True, null=True)
    spasm_duration_description = models.TextField(blank=True, null=True)
    s_febrile_seizure_duration = models.TextField(blank=True, null=True)
    s_febrile_seizure_duration_description = models.TextField(blank=True, null=True)
    c_febrile_seizure_duration = models.TextField(blank=True, null=True)
    c_febrile_seizure_duration_description = models.TextField(blank=True, null=True)

    neonatal_seizure_duration = models.TextField(blank=True, null=True)
    neonatal_seizure_duration_description = models.TextField(blank=True, null=True)
    dependent_epilesy_duration = models.TextField(blank=True, null=True)
    dependent_epilesy_description = models.TextField(blank=True, null=True)
    Familial_infantile_duration = models.TextField(blank=True, null=True)
    Familial_infantile_description = models.TextField(blank=True, null=True)
    dravet_syndrom_duration = models.TextField(blank=True, null=True)
    dravet_syndrom_description = models.TextField(blank=True, null=True)
    glut1_deficiency_duration = models.TextField(blank=True, null=True)
    glut1_deficiency_description = models.TextField(blank=True, null=True)
    fcd_typ_duration = models.TextField(blank=True, null=True)
    fcd_typ_description = models.TextField(blank=True, null=True)
    epileptic_duration = models.TextField(blank=True, null=True)
    epileptic_description = models.TextField(blank=True, null=True)
    eme_duration = models.TextField(blank=True, null=True)
    eme_duration_description = models.TextField(blank=True, null=True)
    eimfs_duration = models.TextField(blank=True, null=True)
    eimfs_duration_description = models.TextField(blank=True, null=True)


    eoee_duration = models.TextField(blank=True, null=True)
    eoee_duration_description = models.TextField(blank=True, null=True)
    infantiles_duration = models.TextField(blank=True, null=True)
    infantiles_duration_description = models.TextField(blank=True, null=True)
    sw_duration = models.TextField(blank=True, null=True)
    sw_duration_description = models.TextField(blank=True, null=True)
    so_duration = models.TextField(blank=True, null=True)
    so_duration_description = models.TextField(blank=True, null=True)
    sd_duration = models.TextField(blank=True, null=True)
    sd_duration_description = models.TextField(blank=True, null=True)
    lgs_duration = models.TextField(blank=True, null=True)
    lgs_duration_description = models.TextField(blank=True, null=True)
    emas_duration = models.TextField(blank=True, null=True)
    emas_duration_description = models.TextField(blank=True, null=True)
    lks_duration = models.TextField(blank=True, null=True)
    lks_duration_description = models.TextField(blank=True, null=True)
    gge_duration = models.TextField(blank=True, null=True)
    gge_duration_description = models.TextField(blank=True, null=True)

    cae_duration = models.TextField(blank=True, null=True)
    cae_duration_description = models.TextField(blank=True, null=True)
    jae_duration = models.TextField(blank=True, null=True)
    jae_duration_description = models.TextField(blank=True, null=True)
    jme_duration = models.TextField(blank=True, null=True)
    jme_duration_description = models.TextField(blank=True, null=True)
    tle_duration = models.TextField(blank=True, null=True)
    tle_duration_description = models.TextField(blank=True, null=True)
    ge_duration = models.TextField(blank=True, null=True)
    ge_duration_description = models.TextField(blank=True, null=True)
    sws_duration = models.TextField(blank=True, null=True)
    sws_duration_description = models.TextField(blank=True, null=True)
    deeswas_duration = models.TextField(blank=True, null=True)
    deeswas_duration_description = models.TextField(blank=True, null=True)
    eesws_duration = models.TextField(blank=True, null=True)
    eeesws_duration_description = models.TextField(blank=True, null=True)
    nm_duration = models.TextField(blank=True, null=True)
    nm_duration_description = models.TextField(blank=True, null=True)

    gms_duration = models.TextField(blank=True, null=True)
    gms_duration_description = models.TextField(blank=True, null=True)
    nfle_duration = models.TextField(blank=True, null=True)
    nfle_duration_description = models.TextField(blank=True, null=True)
    mae_duration = models.TextField(blank=True, null=True)
    mae_duration_description = models.TextField(blank=True, null=True)
    coee_duration = models.TextField(blank=True, null=True)
    coee_duration_description = models.TextField(blank=True, null=True)
    ftle_duration = models.TextField(blank=True, null=True)
    ftle_duration_description = models.TextField(blank=True, null=True)
    bfis_duration = models.TextField(blank=True, null=True)
    bfis_duration_description = models.TextField(blank=True, null=True)
    bfns_duration = models.TextField(blank=True, null=True)
    bfns_duration_description = models.TextField(blank=True, null=True)
    gepd_duration = models.TextField(blank=True, null=True)
    gepd_duration_description = models.TextField(blank=True, null=True)
    dre_duration = models.TextField(blank=True, null=True)
    dre_duration_description = models.TextField(blank=True, null=True)





    # MRI Findings
    mri_findings = models.TextField(blank=True, null=True)
    progressive_microcephaly = models.BooleanField(blank=True, null=True)
    congenital_microcephaly = models.BooleanField(blank=True, null=True)
    focal_brain_malformation = models.BooleanField(blank=True, null=True)
    multifocal_brain_malformation = models.BooleanField(blank=True, null=True)
    polymicrogyria = models.BooleanField(blank=True, null=True)
    asymmetric_polymicrogyria = models.BooleanField(blank=True, null=True)
    optic_nerve_atrophy = models.BooleanField(blank=True, null=True)
    holoprosencephaly = models.BooleanField(blank=True, null=True)
    heterotopia = models.BooleanField(blank=True, null=True)
    subcortical_laminar_heterotopia = models.BooleanField(blank=True, null=True)
    periventricular_heterotopia = models.BooleanField(blank=True, null=True)
    pontocerebellar_hypoplasia = models.BooleanField(blank=True, null=True)
    leucodystrophy = models.BooleanField(blank=True, null=True)
    lissencephaly = models.BooleanField(blank=True, null=True)
    intracranial_hemorrhage = models.BooleanField(blank=True, null=True)
    cerebral_venous_sinus_thrombosis = models.BooleanField(blank=True, null=True)
    atrophy = models.BooleanField(blank=True, null=True)
    hypoplasia_corpus_callosum = models.BooleanField(blank=True, null=True)
    fetal_position = models.CharField(max_length=255, blank=True, null=True)
    corpus_callosum_atrophy = models.BooleanField(blank=True, null=True)
    ventriculomegaly = models.BooleanField(blank=True, null=True)
    white_matter_changes = models.BooleanField(blank=True, null=True)
    gerebral_atrophy = models.BooleanField(blank=True, null=True)
    cerebellar_atrophy = models.BooleanField(blank=True, null=True)
    polimicrogria = models.BooleanField(blank=True, null=True)
    tuberous_sclerosis = models.BooleanField(blank=True, null=True)
    hypothalamic_hamartoma = models.BooleanField(blank=True, null=True)
    basal_ganglia = models.BooleanField(blank=True, null=True)
    hypoxic_ischemic_barin = models.BooleanField(blank=True, null=True)
    hydrocephalus = models.BooleanField(blank=True, null=True)
    development_delay = models.BooleanField(blank=True, null=True)
    development_delay_and_epilepsy = models.TextField(blank=True, null=True)
    epilepsy_only = models.TextField(blank=True, null=True)
    cerebral_atrophy = models.BooleanField(blank=True, null=True)
    basal_ganga = models.BooleanField(blank=True, null=True)

    #eeg
    fed = models.BooleanField(blank=True, null=True)
    g = models.BooleanField(blank=True, null=True)
    fed_g = models.BooleanField(blank=True, null=True)
    swa = models.BooleanField(blank=True, null=True)
    bs = models.BooleanField(blank=True, null=True)
    normal = models.BooleanField(blank=True, null=True)

    # Provocation Factors
    fever = models.BooleanField(blank=True, null=True)
    afebrile_infections = models.BooleanField(blank=True, null=True)
    vaccinations = models.BooleanField(blank=True, null=True)
    emotional_stress = models.BooleanField(blank=True, null=True)
    hot_bathing = models.BooleanField(blank=True, null=True)
    motor_activity = models.BooleanField(blank=True, null=True)
    photostimulation = models.BooleanField(blank=True, null=True)
    hyperventilation = models.BooleanField(blank=True, null=True)

    # Anti-Seizure Medications (ASM)
    br_dose = models.CharField(max_length=100, blank=True, null=True)
    br_description = models.CharField(max_length=100, blank=True, null=True)
    nzp_dose = models.CharField(max_length=100, blank=True, null=True)
    nzp_description = models.CharField(max_length=100, blank=True, null=True)
    cbz_dose = models.CharField(max_length=100, blank=True, null=True)
    cbz_description = models.CharField(max_length=100, blank=True, null=True)
    oxc_dose = models.CharField(max_length=100, blank=True, null=True)
    oxc_description = models.CharField(max_length=100, blank=True, null=True)
    clb_dose = models.CharField(max_length=100, blank=True, null=True)
    clb_description = models.CharField(max_length=100, blank=True, null=True)
    pb_dose = models.CharField(max_length=100, blank=True, null=True)
    pb_description = models.CharField(max_length=100, blank=True, null=True)
    czp_dose = models.CharField(max_length=100, blank=True, null=True)
    czp_description = models.CharField(max_length=100, blank=True, null=True)
    per_dose = models.CharField(max_length=100, blank=True, null=True)
    per_description = models.CharField(max_length=100, blank=True, null=True)
    esm_dose = models.CharField(max_length=100, blank=True, null=True)
    esm_description = models.CharField(max_length=100, blank=True, null=True)
    pgb_dose = models.CharField(max_length=100, blank=True, null=True)
    pgb_description = models.CharField(max_length=100, blank=True, null=True)
    gbp_dose = models.CharField(max_length=100, blank=True, null=True)
    gbp_description = models.CharField(max_length=100, blank=True, null=True)
    pht_dose = models.CharField(max_length=100, blank=True, null=True)
    pht_description = models.CharField(max_length=100, blank=True, null=True)
    lcm_dose = models.CharField(max_length=100, blank=True, null=True)
    lcm_description = models.CharField(max_length=100, blank=True, null=True)
    rfn_dose = models.CharField(max_length=100, blank=True, null=True)
    rfn_description = models.CharField(max_length=100, blank=True, null=True)
    lev_dose = models.CharField(max_length=100, blank=True, null=True)
    lev_description = models.CharField(max_length=100, blank=True, null=True)
    stm_dose = models.CharField(max_length=100, blank=True, null=True)
    stm_description = models.CharField(max_length=100, blank=True, null=True)
    ltg_dose = models.CharField(max_length=100, blank=True, null=True)
    ltg_description = models.CharField(max_length=100, blank=True, null=True)
    stp_dose = models.CharField(max_length=100, blank=True, null=True)
    stp_description = models.CharField(max_length=100, blank=True, null=True)
    lzp_dose = models.CharField(max_length=100, blank=True, null=True)
    lzp_description = models.CharField(max_length=100, blank=True, null=True)
    tpm_dose = models.CharField(max_length=100, blank=True, null=True)
    tpm_description = models.CharField(max_length=100, blank=True, null=True)
    vgb_dose = models.CharField(max_length=100, blank=True, null=True)
    vgb_description = models.CharField(max_length=100, blank=True, null=True)
    vpa_dose = models.CharField(max_length=100, blank=True, null=True)
    vpa_description = models.CharField(max_length=100, blank=True, null=True)
    zns_dose = models.CharField(max_length=100, blank=True, null=True)
    zns_description = models.CharField(max_length=100, blank=True, null=True)

    # Side Effects
    nausea = models.BooleanField(blank=True, null=True)
    vomiting = models.BooleanField(blank=True, null=True)
    rash = models.BooleanField(blank=True, null=True)
    edema = models.BooleanField(blank=True, null=True)
    constipation = models.BooleanField(blank=True, null=True)
    diarrhea = models.BooleanField(blank=True, null=True)
    anorexia = models.BooleanField(blank=True, null=True)
    stomach_pain = models.BooleanField(blank=True, null=True)
    hematological = models.BooleanField(blank=True, null=True)
    obesity = models.BooleanField(blank=True, null=True)
    drowsiness = models.BooleanField(blank=True, null=True)
    hyperactivity = models.BooleanField(blank=True, null=True)
    skin_manifestations = models.BooleanField(blank=True, null=True)

    response_50_74_2 = models.BooleanField(blank=True, null=True)
    response_75_99_2 = models.BooleanField(blank=True, null=True)
    response_100_2 = models.BooleanField(blank=True, null=True)
    non_response_2 = models.BooleanField(blank=True, null=True)
    aggravation_2 = models.BooleanField(blank=True, null=True)

    # Anti-Hormonal Therapy
    methyl_prednisolone_dose = models.CharField(max_length=100, blank=True, null=True)
    methyl_prednisolone_description = models.CharField(max_length=100, blank=True, null=True)
    prednisolone_dose = models.CharField(max_length=100, blank=True, null=True)
    prednisolone_description = models.CharField(max_length=100, blank=True, null=True)
    dexamethasone_dose = models.CharField(max_length=100, blank=True, null=True)
    dexamethasone_description = models.CharField(max_length=100, blank=True, null=True)
    acth_dose = models.CharField(max_length=100, blank=True, null=True)
    acth_description = models.CharField(max_length=100, blank=True, null=True)
    hydrocortisone_dose = models.CharField(max_length=100, blank=True, null=True)
    hydrocortisone_description = models.CharField(max_length=100, blank=True, null=True)

    #wes
    wes = models.BooleanField(blank=True, null=True)
    pathogenic = models.TextField(blank=True, null=True)
    like_pathogenic = models.TextField(blank=True, null=True)
    vus = models.TextField(blank=True, null=True)

    # Treatment Response
    response_50_74 = models.BooleanField(blank=True, null=True)
    response_75_99 = models.BooleanField(blank=True, null=True)
    response_100 = models.BooleanField(blank=True, null=True)
    non_response = models.BooleanField(blank=True, null=True)
    aggravation = models.BooleanField(blank=True, null=True)

    # Medication Compliance
    medication_missed = models.BooleanField(blank=True, null=True)
    medication_missed_description = models.TextField(blank=True, null=True)
    other_medications_triggered_attack = models.BooleanField(blank=True, null=True)
    other_medications_description = models.TextField(blank=True, null=True)

    # Pharmacoresistance
    farmacoresistant = models.BooleanField(blank=True, null=True)
    change_of_2_aep = models.BooleanField(blank=True, null=True)
    change_of_more_than_2_aep = models.BooleanField(blank=True, null=True)
    monotherapy = models.BooleanField(blank=True, null=True)
    duotherapy = models.BooleanField(blank=True, null=True)
    polytherapy = models.BooleanField(blank=True, null=True)

    # Additional Examinations
    nsg = models.TextField(blank=True, null=True)
    audiogram = models.TextField(blank=True, null=True)
    ophthalmologist = models.TextField(blank=True, null=True)
    genetic = models.TextField(blank=True, null=True)

    # Recommendations
    recommendations = models.TextField(blank=True, null=True)

    # Clinical Diagnosis
    clinical_diagnosis = models.TextField(blank=True, null=True)

    # Notes
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name or "Unnamed Patient"
