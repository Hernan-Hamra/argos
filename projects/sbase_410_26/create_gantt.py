import sys
sys.stdout.reconfigure(encoding='utf-8')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# Phases with start and end days
phases = [
    ('Ingeniería de detalle\ny relevamiento', 1, 5),
    ('Aprovisionamiento\nde materiales', 1, 7),
    ('Canalización y\nmontaje de racks', 6, 15),
    ('Cableado estructurado\ny fibra óptica', 12, 25),
    ('Instalación de\nequipamiento activo', 22, 30),
    ('Configuración y\npuesta en marcha', 28, 40),
    ('Certificación, pruebas\ny documentación', 38, 45),
]

# Colors - professional blue gradient
colors = [
    '#1B4F72', '#2471A3', '#2E86C1', '#3498DB',
    '#5DADE2', '#85C1E9', '#AED6F1'
]

fig, ax = plt.subplots(figsize=(12, 5))

y_positions = list(range(len(phases) - 1, -1, -1))

for i, (name, start, end) in enumerate(phases):
    duration = end - start + 1
    y = y_positions[i]

    # Draw bar
    bar = ax.barh(y, duration, left=start - 0.5, height=0.6,
                  color=colors[i], edgecolor='white', linewidth=1.5,
                  zorder=3)

    # Add duration text on bar
    ax.text(start + duration/2 - 0.5, y, f'{duration}d',
            ha='center', va='center', fontsize=9, fontweight='bold',
            color='white', zorder=4)

# Labels
ax.set_yticks(y_positions)
ax.set_yticklabels([p[0] for p in phases], fontsize=9, fontfamily='sans-serif')

# X axis - weeks
ax.set_xlim(0, 46)
ax.set_xlabel('Días corridos', fontsize=10, fontweight='bold')

# Week markers
for week in range(7, 46, 7):
    ax.axvline(x=week, color='#D5D8DC', linewidth=0.8, linestyle='--', zorder=1)

# Semana labels on top
ax2 = ax.twiny()
ax2.set_xlim(ax.get_xlim())
week_positions = [3.5, 10.5, 17.5, 24.5, 31.5, 38.5, 45]
week_labels = ['Sem 1', 'Sem 2', 'Sem 3', 'Sem 4', 'Sem 5', 'Sem 6', 'Sem 7']
ax2.set_xticks(week_positions[:len(week_labels)])
ax2.set_xticklabels(week_labels, fontsize=8, color='#5D6D7E')

# Title
ax.set_title('Cronograma de Ejecución - LP 410/26 SBASE\nPlazo total: 45 días corridos',
             fontsize=12, fontweight='bold', pad=25, color='#1B4F72')

# Grid
ax.grid(axis='x', alpha=0.3, zorder=0)
ax.set_axisbelow(True)

# Style
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

plt.tight_layout()

output = r'C:\Users\HERNAN\argos\gantt_sbd.png'
fig.savefig(output, dpi=200, bbox_inches='tight', facecolor='white')
plt.close()
print(f'Gantt saved: {output}')
