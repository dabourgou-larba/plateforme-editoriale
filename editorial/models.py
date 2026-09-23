from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.Model):
    """Un rôle métier : correspondant, rédacteur, correcteur, responsable,
    commercial ou diffuseur. Détermine les permissions de l'utilisateur."""

    CORRESPONDANT = "correspondant"
    REDACTEUR = "redacteur"
    CORRECTEUR = "correcteur"
    RESPONSABLE = "responsable"
    COMMERCIAL = "commercial"
    DIFFUSEUR = "diffuseur"

    CHOICES = [
        (CORRESPONDANT, "Correspondant"),
        (REDACTEUR, "Rédacteur"),
        (CORRECTEUR, "Correcteur"),
        (RESPONSABLE, "Responsable de service"),
        (COMMERCIAL, "Service commercial"),
        (DIFFUSEUR, "Diffuseur"),
    ]

    nom = models.CharField(max_length=30, choices=CHOICES, unique=True)

    def __str__(self):
        return self.get_nom_display()


class Utilisateur(AbstractUser):
    """Utilisateur de la plateforme, rattaché à un rôle unique.
    Étend le modèle utilisateur standard de Django (login, mot de passe, etc.)."""

    role = models.ForeignKey(Role, on_delete=models.PROTECT, related_name="utilisateurs")
    telephone = models.CharField(max_length=20, blank=True)
    localisation = models.CharField(max_length=100, blank=True, help_text="Zone de couverture du correspondant, le cas échéant")

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.role})"


class Categorie(models.Model):
    nom = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = "Catégories"

    def __str__(self):
        return self.nom


class Depeche(models.Model):
    """Une dépêche et son cycle de vie éditorial."""

    BROUILLON = "brouillon"
    SOUMISE = "soumise"
    EN_REDACTION = "en_redaction"
    EN_CORRECTION = "en_correction"
    VALIDEE = "validee"
    PUBLIEE = "publiee"
    ARCHIVEE = "archivee"

    STATUTS = [
        (BROUILLON, "Brouillon"),
        (SOUMISE, "Soumise"),
        (EN_REDACTION, "En rédaction"),
        (EN_CORRECTION, "En correction"),
        (VALIDEE, "Validée"),
        (PUBLIEE, "Publiée"),
        (ARCHIVEE, "Archivée"),
    ]

    titre = models.CharField(max_length=255)
    chapo = models.CharField(max_length=500, blank=True, help_text="Chapô ajouté par le rédacteur")
    contenu = models.TextField()
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True, related_name="depeches")
    auteur = models.ForeignKey(Utilisateur, on_delete=models.PROTECT, related_name="depeches_creees")
    statut = models.CharField(max_length=20, choices=STATUTS, default=BROUILLON)
    note_rejet = models.TextField(blank=True, help_text="Motif de rejet renseigné par le correcteur")
    lieu_evenement = models.CharField(max_length=150, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date_creation"]
        verbose_name_plural = "Dépêches"

    def __str__(self):
        return f"{self.titre} [{self.get_statut_display()}]"


class Media(models.Model):
    PHOTO = "photo"
    AUDIO = "audio"
    VIDEO = "video"
    TYPES = [(PHOTO, "Photo"), (AUDIO, "Audio"), (VIDEO, "Vidéo")]

    depeche = models.ForeignKey(Depeche, on_delete=models.CASCADE, related_name="medias")
    type = models.CharField(max_length=10, choices=TYPES)
    fichier = models.FileField(upload_to="medias/%Y/%m/")
    legende = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.type} - {self.depeche.titre}"


class Historique(models.Model):
    """Journal d'actions pour la traçabilité complète d'une dépêche."""

    depeche = models.ForeignKey(Depeche, on_delete=models.CASCADE, related_name="historique")
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True, related_name="actions")
    action = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["date"]
        verbose_name_plural = "Historique"

    def __str__(self):
        return f"{self.action} — {self.date:%d/%m/%Y %H:%M}"


class Client(models.Model):
    TYPES = [("media", "Média partenaire"), ("institution", "Institutionnel"), ("particulier", "Particulier")]

    nom = models.CharField(max_length=150)
    type = models.CharField(max_length=20, choices=TYPES)
    contact_email = models.EmailField(blank=True)
    contact_telephone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.nom


class Abonnement(models.Model):
    FLUX_TEMPS_REEL = "flux_temps_reel"
    ACCES_ARCHIVES = "acces_archives"
    COMPLET = "complet"
    TYPES = [
        (FLUX_TEMPS_REEL, "Flux temps réel"),
        (ACCES_ARCHIVES, "Accès archives"),
        (COMPLET, "Accès complet"),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="abonnements")
    type_abonnement = models.CharField(max_length=20, choices=TYPES)
    date_debut = models.DateField()
    date_fin = models.DateField(null=True, blank=True)
    actif = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.client} — {self.get_type_abonnement_display()}"


class Diffusion(models.Model):
    SITE_WEB = "site_web"
    API = "api"
    RSS = "rss"
    CANAUX = [(SITE_WEB, "Site web"), (API, "API partenaires"), (RSS, "Flux RSS")]

    depeche = models.ForeignKey(Depeche, on_delete=models.CASCADE, related_name="diffusions")
    canal = models.CharField(max_length=20, choices=CANAUX)
    date_diffusion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.depeche.titre} via {self.get_canal_display()}"
