import os
import django
from django.db.models import Q

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from email_manager.models import Email

def audit_absences():
    keywords = [
        "malade", "sick", "gastro", "garderie", "daycare", "enfant", "daughter", "son", "fille", "fils",
        "vaccin", "clinique", "clinic", "médecin", "doctor", "docteur", "rester", "staying", "maison", "home",
        "conge", "absence", "pédiatre", "pediatrician"
    ]
    
    query = Q()
    for kw in keywords:
        query |= Q(body_plain_text__icontains=kw) | Q(subject__icontains=kw)
        
    # Filter by LP as sender and relevant period
    emails = Email.objects.filter(query, sender_protagonist_id=1, date_sent__year__range=(2009, 2015)).order_by('date_sent')
    
    documented_absences = []
    
    for e in emails:
        body = e.body_plain_text.lower() if e.body_plain_text else ""
        subject = e.subject.lower() if e.subject else ""
        text = subject + " " + body
        
        # Look for explicit mention of staying home OR missing work AND mention of child/illness
        is_absence = False
        reason = ""
        
        # Child indicators
        child_ref = any(w in text for w in ["fille", "fils", "enfant", "alexia", "nicolas", "daughter", "son", "petite", "petit", "gars"])
        # Absence indicators
        absence_ref = any(w in text for w in ["rester", "staying", "pas rentrer", "pas au travail", "pas venir", "not coming", "absence", "conge", "conge", "maladie", "home", "maison"])
        # Medical/Care indicators
        care_ref = any(w in text for w in ["malade", "sick", "gastro", "vaccin", "clinique", "clinic", "medecin", "doctor", "docteur", "pediatre", "garderie", "daycare"])
        
        if absence_ref and (child_ref or care_ref):
            is_absence = True
            
        if is_absence:
            # Avoid duplicates on same day if multiple emails sent
            date_str = e.date_sent.strftime('%Y-%m-%d')
            if not documented_absences or documented_absences[-1]['date'] != date_str:
                documented_absences.append({
                    'date': date_str,
                    'subject': e.subject,
                    'excerpt': e.body_plain_text[:150].replace('\n', ' ') if e.body_plain_text else ""
                })

    print(f"Total documented unique days of absence/WFH for childcare: {len(documented_absences)}")
    for d in documented_absences:
        print(f"- {d['date']}: {d['subject']} | {d['excerpt']}")

if __name__ == "__main__":
    audit_absences()
