from django.db import models
from django.core.exceptions import ValidationError


class Professeur(models.Model):
    cin_prof = models.CharField(
        primary_key=True, 
        max_length=20, 
        verbose_name="CIN du professeur",
        unique=True
    )
    nom_prof = models.CharField(max_length=255, verbose_name="Nom du professeur")
    email_prof = models.EmailField(verbose_name="Email du professeur", unique=True)
    num_tele_prof = models.CharField(
        max_length=15, 
        verbose_name="Numéro de téléphone", 
        unique=True
    )
    fonction_prof = models.CharField(max_length=255, verbose_name="Fonction du professeur")

    def __str__(self):
        return self.nom_prof

    class Meta:
        verbose_name = "Professeur"
        verbose_name_plural = "Professeurs"
        ordering = ['nom_prof']


class Departement(models.Model):
    id_dept = models.AutoField(primary_key=True)
    nom_departement = models.CharField(
        max_length=255, 
        verbose_name="Nom du département", 
        unique=True
    )
    coordonateur_dept = models.ForeignKey(
        Professeur,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="coordonateur_departements",
        verbose_name="Coordonateur du département"
    )

    def __str__(self):
        return self.nom_departement

    class Meta:
        verbose_name = "Département"
        verbose_name_plural = "Départements"
        ordering = ['nom_departement']


class Filiere(models.Model):
    id_filiere = models.AutoField(primary_key=True)
    type_diplome = models.CharField(max_length=255, verbose_name="Type de diplôme")
    nom_filiere = models.CharField(max_length=255, verbose_name="Nom de la filière", unique=True)
    description_filiere = models.TextField(verbose_name="Description de la filière", blank=True)
    respo_filiere = models.ForeignKey(
        Professeur,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="responsable_filieres",
        verbose_name="Responsable de la filière"
    )
    equipe_pedagogique = models.ManyToManyField(
        Professeur, 
        through="ResponsabiliteModule", 
        related_name="equipes_pedagogiques",
        verbose_name="Équipe pédagogique"
    )
    nombre_sem = models.PositiveIntegerField(verbose_name="Nombre de semestres")
    id_departement = models.ForeignKey(
        Departement, 
        on_delete=models.CASCADE, 
        verbose_name="Département"
    )

    def clean(self):
        """Validation des champs."""
        if self.nombre_sem < 1:
            raise ValidationError("Le nombre de semestres doit être au moins égal à 1.")

    def __str__(self):
        return self.nom_filiere

    class Meta:
        verbose_name = "Filière"
        verbose_name_plural = "Filières"
        ordering = ['nom_filiere']


class Semestre(models.Model):
    id_sem = models.AutoField(primary_key=True)
    num_sem = models.PositiveIntegerField(verbose_name="Numéro du semestre")
    id_filiere = models.ForeignKey(
        Filiere, 
        on_delete=models.CASCADE, 
        verbose_name="Filière"
    )
    nombre_modules = models.PositiveIntegerField(verbose_name="Nombre de modules")

    def clean(self):
        """Validation des champs."""
        if self.nombre_modules < 1:
            raise ValidationError("Le nombre de modules doit être au moins égal à 1.")

    def __str__(self):
        return f"Semestre {self.num_sem} - {self.id_filiere.nom_filiere}"

    class Meta:
        verbose_name = "Semestre"
        verbose_name_plural = "Semestres"
        ordering = ['id_filiere', 'num_sem']


class Module(models.Model):
    id_module = models.AutoField(primary_key=True)
    num_module = models.PositiveIntegerField(verbose_name="Numéro du module")
    nom_module = models.CharField(max_length=255, verbose_name="Nom du module")
    charge_horaire = models.DurationField(verbose_name="Charge horaire")
    nombre_elements = models.PositiveIntegerField(verbose_name="Nombre d'éléments")
    coefficient_module = models.PositiveIntegerField(verbose_name="Coefficient du module")
    id_sem = models.ForeignKey(
        Semestre, 
        on_delete=models.CASCADE, 
        verbose_name="Semestre"
    )
    respo_module = models.ForeignKey(
        Professeur,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="modules_responsables",
        verbose_name="Responsable du module"
    )

    def __str__(self):
        return self.nom_module

    class Meta:
        verbose_name = "Module"
        verbose_name_plural = "Modules"
        ordering = ['id_sem', 'num_module']


class ResponsabiliteModule(models.Model):
    professeur = models.ForeignKey(
        Professeur, 
        on_delete=models.CASCADE, 
        verbose_name="Professeur"
    )
    filiere = models.ForeignKey(
        Filiere, 
        on_delete=models.CASCADE, 
        verbose_name="Filière"
    )
    module = models.ForeignKey(
        Module, 
        on_delete=models.CASCADE, 
        verbose_name="Module"
    )

    def __str__(self):
        return f"{self.professeur.nom_prof} - {self.module.nom_module} ({self.filiere.nom_filiere})"

    class Meta:
        verbose_name = "Responsabilité Module"
        verbose_name_plural = "Responsabilités Modules"
        unique_together = ('professeur', 'filiere', 'module')


class Element(models.Model):
    id_element = models.AutoField(primary_key=True)
    nom_element = models.CharField(max_length=255, verbose_name="Nom de l'élément")
    num_element = models.PositiveIntegerField(verbose_name="Numéro de l'élément")
    heure_tp = models.DurationField(verbose_name="Durée TP")
    heure_td = models.DurationField(verbose_name="Durée TD")
    heure_cours = models.DurationField(verbose_name="Durée Cours")
    ponderation_element = models.PositiveIntegerField(verbose_name="Pondération")
    id_module = models.ForeignKey(
        Module, 
        on_delete=models.CASCADE, 
        verbose_name="Module"
    )

    def __str__(self):
        return self.nom_element

    class Meta:
        verbose_name = "Élément"
        verbose_name_plural = "Éléments"
        ordering = ['id_module', 'num_element']
