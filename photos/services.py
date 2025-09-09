import os
import io
from datetime import datetime
from django.utils import timezone
from django.core.files.base import ContentFile
from PIL import Image
import exifread
import rawpy
import piexif

from .models import Photo

class PhotoProcessingService:
    """
    A service class containing the end-to-end logic for processing a photo file.
    """
    def __init__(self):
        self.supported_extensions = ('.jpg', '.jpeg', '.cr2')
        self.max_width = 1600
        self.jpeg_quality = 90

    def _parse_date(self, tags):
        for key in ('EXIF DateTimeOriginal', 'Image DateTime', 'EXIF DateTimeDigitized'):
            if key in tags:
                try:
                    dt_str = str(tags[key].values)
                    dt_naive = datetime.strptime(dt_str, "%Y:%m:%d %H:%M:%S")
                    return timezone.make_aware(dt_naive)
                except (ValueError, TypeError, AttributeError):
                    continue
        return None

    def _to_float(self, val):
        if val is None: return None
        try:
            # exifread.utils.Ratio object has .values list with one Ratio object
            if hasattr(val, 'values') and isinstance(val.values, list) and len(val.values) > 0:
                ratio = val.values[0]
                if hasattr(ratio, 'num'): # It's a Ratio
                    return float(ratio.num) / float(ratio.den)
                return float(ratio)
            # Handle direct strings or numbers
            val_str = str(val)
            if '/' in val_str:
                num, den = val_str.split('/')
                return float(num) / float(den)
            return float(val_str)
        except (ValueError, TypeError, ZeroDivisionError, AttributeError): return None

    def _to_int(self, val):
        if val is None: return None
        try: 
            # exifread returns a list for some integer values
            if hasattr(val, 'values') and isinstance(val.values, list) and len(val.values) > 0:
                return int(val.values[0])
            # --- FIXED: Safely handle None from _to_float ---
            float_val = self._to_float(val)
            if float_val is None:
                return None
            return int(float_val)
        except (ValueError, TypeError, AttributeError): return None

    def process_photo_file(self, source_path: str, date_from_folder=None, photo_type=None):
        if not os.path.exists(source_path):
            return None

        original_filename = os.path.basename(source_path)

        try:
            with open(source_path, 'rb') as f:
                tags = exifread.process_file(f, details=False)
        except Exception:
            return None

        datetime_original = self._parse_date(tags)
        if not datetime_original:
            return None

        if original_filename.lower().endswith('.cr2'):
            with rawpy.imread(source_path) as raw:
                rgb = raw.postprocess()
            img = Image.fromarray(rgb)
        else:
            img = Image.open(source_path)

        w, h = img.size
        if w > self.max_width:
            new_h = int(h * self.max_width / w)
            img = img.resize((self.max_width, new_h), Image.Resampling.LANCZOS)

        exif_dict = {"Exif": {piexif.ExifIFD.DateTimeOriginal: datetime_original.strftime("%Y:%m:%d %H:%M:%S").encode()}}
        exif_bytes = piexif.dump(exif_dict)

        buffer = io.BytesIO()
        img.save(buffer, "JPEG", quality=self.jpeg_quality, exif=exif_bytes)
        processed_image_bytes = buffer.getvalue()

        photo = Photo(
            file_path=source_path,
            file_name=original_filename,
            datetime_original=datetime_original,
            date_folder=date_from_folder,
            photo_type=photo_type,
            make=str(tags.get('Image Make', '')),
            model=str(tags.get('Image Model', '')),
            # FIXED: Pass the tag object directly to the conversion helpers
            iso_speed=self._to_int(tags.get('EXIF ISOSpeedRatings')),
            exposure_time=str(tags.get('EXIF ExposureTime', '')),
            f_number=self._to_float(tags.get('EXIF FNumber')),
            focal_length=self._to_float(tags.get('EXIF FocalLength')),
            lens_model=str(tags.get('EXIF LensModel', '')),
        )
        
        new_filename = f"{os.path.splitext(original_filename)[0]}.jpg"
        photo.file.save(new_filename, ContentFile(processed_image_bytes), save=True)
        
        return photo
