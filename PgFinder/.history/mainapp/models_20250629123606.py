from django.db import models

# Create your models here.

class PGInformation(models.Model):
    # Basic Info
    pgname = models.CharField(max_length=100)
    ownername = models.CharField(max_length=100)
    mail = models.EmailField()
    password = models.CharField(max_length=100)
   

    # Bathroom Type - Select Option
    BATHROOM_CHOICES = [
        ('common', 'Common Bathrooms'),
        ('attached', 'Attached Bathrooms'),
        ('both', 'Both'),
    ]
    AREA_CHOICES = [
    ("Anekal", "Anekal"),
    ("Anjanapura", "Anjanapura"),
    ("Arekere", "Arekere"),
    ("Attibele", "Attibele"),
    ("Balepet", "Balepet"),
    ("Banashankari", "Banashankari"),
    ("Banaswadi", "Banaswadi"),
    ("Basavanagudi", "Basavanagudi"),
    ("Basaveshwaranagar", "Basaveshwaranagar"),
    ("Begur", "Begur"),
    ("Bellandur", "Bellandur"),
    ("Bommanahalli", "Bommanahalli"),
    ("Bommasandra", "Bommasandra"),
    ("BTM Layout", "BTM Layout"),
    ("Chandapura", "Chandapura"),
    ("Chickpet", "Chickpet"),
    ("Chikkabanavara", "Chikkabanavara"),
    ("Cottonpet", "Cottonpet"),
    ("CV Raman Nagar", "CV Raman Nagar"),
    ("Domlur", "Domlur"),
    ("Electronic City", "Electronic City"),
    ("Fraser Town (Pulakeshi Nagar)", "Fraser Town (Pulakeshi Nagar)"),
    ("Girinagar", "Girinagar"),
    ("Gottigere", "Gottigere"),
    ("Hebbal", "Hebbal"),
    ("HBR Layout", "HBR Layout"),
    ("Hesaraghatta", "Hesaraghatta"),
    ("Hoodi", "Hoodi"),
    ("Horamavu", "Horamavu"),
    ("HSR Layout", "HSR Layout"),
    ("Hulimavu", "Hulimavu"),
    ("Indiranagar", "Indiranagar"),
    ("J. P. Nagar", "J. P. Nagar"),
    ("Jalahalli", "Jalahalli"),
    ("Jayanagar", "Jayanagar"),
    ("Jigani", "Jigani"),
    ("Kalyan Nagar", "Kalyan Nagar"),
    ("Kamakshipalya", "Kamakshipalya"),
    ("Kammanahalli", "Kammanahalli"),
    ("Kengeri", "Kengeri"),
    ("Koramangala", "Koramangala"),
    ("Kothnur", "Kothnur"),
    ("Krishnarajapuram", "Krishnarajapuram"),
    ("Kumaraswamy Layout", "Kumaraswamy Layout"),
    ("Lingarajapuram", "Lingarajapuram"),
    ("Madiwala", "Madiwala"),
    ("Mahalakshmi Layout", "Mahalakshmi Layout"),
    ("Mahadevapura", "Mahadevapura"),
    ("Malleswaram", "Malleswaram"),
    ("Marathahalli", "Marathahalli"),
    ("Mathikere", "Mathikere"),
    ("Nagarbhavi", "Nagarbhavi"),
    ("Nandini Layout", "Nandini Layout"),
    ("Nayandahalli", "Nayandahalli"),
    ("Nelamangala", "Nelamangala"),
    ("Padmanabhanagar", "Padmanabhanagar"),
    ("Peenya", "Peenya"),
    ("Pete Area (Chickpet, Balepet, Cottonpet, Sultanpet)", "Pete Area (Chickpet, Balepet, Cottonpet, Sultanpet)"),
    ("R. T. Nagar", "R. T. Nagar"),
    ("Rajarajeshwari Nagar", "Rajarajeshwari Nagar"),
    ("Rajajinagar", "Rajajinagar"),
    ("Ramamurthy Nagar", "Ramamurthy Nagar"),
    ("Sadashivanagar", "Sadashivanagar"),
    ("Sarjapura", "Sarjapura"),
    ("Seshadripuram", "Seshadripuram"),
    ("Shivajinagar", "Shivajinagar"),
    ("Sultanpet", "Sultanpet"),
    ("Thavarekere", "Thavarekere"),
    ("Ulsoor (Halasuru)", "Ulsoor (Halasuru)"),
    ("Uttarahalli", "Uttarahalli"),
    ("Varthur", "Varthur"),
    ("Vasanth Nagar", "Vasanth Nagar"),
    ("Vidyaranyapura", "Vidyaranyapura"),
    ("Vijayanagar", "Vijayanagar"),
    ("Whitefield", "Whitefield"),
    ("Yelahanka", "Yelahanka"),
    ("Yeshwanthpur", "Yeshwanthpur"),
]
    area = models.CharField(max_length=100,choices=AREA_CHOICES)

    bathroom_type = models.CharField(max_length=10, choices=BATHROOM_CHOICES)

    # Checkboxes - Facilities
    washing_machine = models.BooleanField(default=False)
    water_heater = models.BooleanField(default=False)
    ac = models.BooleanField(default=False)

    # Languages Known
    languageknown1 = models.CharField(max_length=50, blank=True)
    languageknown2 = models.CharField(max_length=50, blank=True)
    languageknown3 = models.CharField(max_length=50, blank=True)

    # Sharing Type Checkboxes  Vacancies and Fees
    two_sharing = models.BooleanField(default=False)
    vacancy2 = models.IntegerField(null=True, blank=True)
    fees2 = models.IntegerField(null=True, blank=True)

    three_sharing = models.BooleanField(default=False)
    vacancy3 = models.IntegerField(null=True, blank=True)
    fees3 = models.IntegerField(null=True, blank=True)

    four_sharing = models.BooleanField(default=False)
    vacancy4 = models.IntegerField(null=True, blank=True)
    fees4 = models.IntegerField(null=True, blank=True)


    other_sharing = models.BooleanField(default=False)
    vacancy = models.IntegerField(null=True, blank=True)
    fees = models.IntegerField(null=True, blank=True)

    # Contact
    phno = models.CharField(max_length=15)

    # Address
    address = models.TextField()

    def __str__(self):
        return self.pgname
class PGImage(models.Model):
    image=models.Field(upload_to='pg_images/')
    pg=models.ForeignKey(PGInformation,on_delete=models.CASCADE,related_name='images')

