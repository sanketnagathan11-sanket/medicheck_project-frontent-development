c = open('MediCheck.html', encoding='utf-8').read()

# 1. Add id to tier-section
c = c.replace('<div class="tier-section">', '<div class="tier-section" id="tailored-service-tiers">')

# 2. Add onclick to the tags in footer
old_tags = """<div class="tag-strip">
        <span class="lab-tag">MASS WALK-IN TIER</span>
        <span class="lab-tag lab-tag-p">PREMIUM HOME COLLECTION TIER</span>
      </div>"""

new_tags = """<div class="tag-strip">
        <span class="lab-tag" style="cursor:pointer;" onclick="showPage('home'); setTimeout(() => { document.getElementById('tailored-service-tiers').scrollIntoView({behavior: 'smooth'}) }, 50);">MASS WALK-IN TIER</span>
        <span class="lab-tag lab-tag-p" style="cursor:pointer;" onclick="showPage('home'); setTimeout(() => { document.getElementById('tailored-service-tiers').scrollIntoView({behavior: 'smooth'}) }, 50);">PREMIUM HOME COLLECTION TIER</span>
      </div>"""

c = c.replace(old_tags, new_tags)

open('MediCheck.html', 'w', encoding='utf-8').write(c)
