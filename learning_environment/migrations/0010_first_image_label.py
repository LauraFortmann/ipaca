from django.db import migrations, models


def create_image_label(apps, schema_editor):
    """
    In this method a PartnerPreferences Questionaire is created.
    """
  
    Image_Label = apps.get_model("learning_environment", "Image_Label")


    # filter the pp questionnaire
    image_label = Image_Label.objects.create(
        name = "dentists",
        url = "OIP.jpg",
        label = "child, dentist, assistant, teeth, instrument"
    )



def undo_create_image_label(apps, schema_editor):
    """
    This function should always be implemented so that we can migrate back and forth as we want.
    """
    Image_Label = apps.get_model("leanrning_environment", "Image_Label")


    image_label = Image_Label.objects.get(
        name = "dentists"
    ).delete()

    

class Migration(migrations.Migration):

    dependencies = [
        # Add the previous migration here.
        # Dependencies are a tuple: (app_name, migration_name).
        ('learning_environment', '0009_image_label'),
    ]

    operations = [
        # Here you define the schedule of your migrations.
        # When you have written custom methods like we did, we need migrations.RunPython.
        # There you have to add your forward method and the backward method.
        migrations.RunPython(create_image_label, reverse_code=undo_create_image_label),
    ]

