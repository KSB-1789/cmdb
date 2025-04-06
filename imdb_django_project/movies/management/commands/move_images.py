import os
import shutil
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Move images from media/static/images to media/images'

    def handle(self, *args, **options):
        source_dir = os.path.join(settings.MEDIA_ROOT, 'static', 'images')
        target_dir = os.path.join(settings.MEDIA_ROOT, 'images')

        # Create target directory if it doesn't exist
        os.makedirs(target_dir, exist_ok=True)

        # Move all files from source to target
        for filename in os.listdir(source_dir):
            source_path = os.path.join(source_dir, filename)
            target_path = os.path.join(target_dir, filename)
            
            if os.path.isfile(source_path):
                shutil.move(source_path, target_path)
                self.stdout.write(self.style.SUCCESS(f'Moved {filename}'))

        # Remove empty source directory
        if not os.listdir(source_dir):
            os.rmdir(source_dir)
            os.rmdir(os.path.dirname(source_dir))

        self.stdout.write(self.style.SUCCESS('Successfully moved all images')) 