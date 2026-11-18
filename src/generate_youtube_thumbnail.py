"""
generate_youtube_thumbnail.py
Generates a crisp, broadcast-grade 1280x720 YouTube thumbnail tailored to Rajasthan Royals branding.
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'outputs')
os.makedirs(OUTPUT_DIR, exist_ok=True)
OUTPUT_PATH = os.path.join(OUTPUT_DIR, 'youtube_thumbnail.png')

# 1280 x 720 Standard YouTube Thumbnail
fig = plt.figure(figsize=(12.8, 7.2), dpi=100)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 1280)
ax.set_ylim(0, 720)
ax.axis('off')

# Custom Dark Gradient Background
X = np.linspace(0, 1, 1280)
Y = np.linspace(0, 1, 720)
base_color = np.zeros((720, 1280, 3))
for i in range(720):
    for j in range(1280):
        t = j / 1280.0
        # Dark Navy (#0B132B) to Midnight Blue (#0F1E3D)
        base_color[i, j] = [
            (11 + 8 * (1 - t)) / 255.0,
            (19 + 20 * (1 - t)) / 255.0,
            (43 + 45 * (1 - t)) / 255.0
        ]

ax.imshow(base_color, aspect='auto', origin='lower')

# Top accent bar in Royal Pink (#E91E63)
ax.add_patch(patches.Rectangle((0, 706), 1280, 14, color='#E91E63', zorder=5))
# Bottom subtle gold accent line
ax.add_patch(patches.Rectangle((0, 0), 1280, 8, color='#F59E0B', zorder=5))

# Top Left Tag: RAJASTHAN ROYALS | SUPERR SELECTOR SEASON 2
ax.add_patch(patches.FancyBboxPatch((60, 620), 490, 48, boxstyle="round,pad=8", fc='#E91E63', ec='none', zorder=10))
ax.text(305, 644, "RAJASTHAN ROYALS | SUPERR SELECTOR S2", color='white', fontsize=16, fontweight='heavy', ha='center', va='center', zorder=11)

# Main Hook Headline: 2 lines
ax.text(60, 520, "CRACKING THE", color='#F8FAFC', fontsize=48, fontweight='heavy', ha='left', va='center', zorder=10)
ax.text(60, 430, "CLUTCH CODE", color='#E91E63', fontsize=64, fontweight='heavy', ha='left', va='center', zorder=10)

# Subtitle / Model Badge
ax.text(60, 345, "Top 10 Pressure Performers in T20 Cricket", color='#CBD5E1', fontsize=22, fontweight='bold', ha='left', va='center', zorder=10)

# Feature highlights badges
ax.add_patch(patches.FancyBboxPatch((60, 240), 220, 55, boxstyle="round,pad=6", fc='#1E3A8A', ec='#3B82F6', lw=1.5, zorder=10))
ax.text(170, 267, "200K+ Deliveries", color='white', fontsize=15, fontweight='bold', ha='center', va='center', zorder=11)

ax.add_patch(patches.FancyBboxPatch((300, 240), 220, 55, boxstyle="round,pad=6", fc='#1E3A8A', ec='#3B82F6', lw=1.5, zorder=10))
ax.text(410, 267, "5-Pillar Consensus", color='white', fontsize=15, fontweight='bold', ha='center', va='center', zorder=11)

ax.add_patch(patches.FancyBboxPatch((540, 240), 220, 55, boxstyle="round,pad=6", fc='#1E3A8A', ec='#3B82F6', lw=1.5, zorder=10))
ax.text(650, 267, "Bayesian Model", color='#F59E0B', fontsize=15, fontweight='bold', ha='center', va='center', zorder=11)

# Author Credit at bottom left
ax.text(60, 150, "By Sahil Advani | Strategy Presentation for Giles Lindsay and Kumar Sangakkara", color='#94A3B8', fontsize=13, fontweight='bold', ha='left', va='center', zorder=10)

# Right Side Card: SHOWCASING #1 PERFORMERS
ax.add_patch(patches.FancyBboxPatch((820, 110), 400, 530, boxstyle="round,pad=15", fc='#0B132B', ec='#E91E63', lw=3, zorder=10))
ax.text(1020, 595, "OFFICIAL CONSENSUS #1s", color='#F59E0B', fontsize=16, fontweight='heavy', ha='center', va='center', zorder=11)

# #1 Batter Box
ax.add_patch(patches.FancyBboxPatch((850, 360), 340, 200, boxstyle="round,pad=10", fc='#131E3A', ec='#E91E63', lw=1.5, zorder=11))
ax.text(1020, 525, "TOP CLUTCH BATTER", color='#E91E63', fontsize=14, fontweight='heavy', ha='center', va='center', zorder=12)
ax.text(1020, 475, "DONOVAN FERREIRA", color='white', fontsize=21, fontweight='heavy', ha='center', va='center', zorder=12)
ax.text(1020, 425, "193.70 Strike Rate", color='#38BDF8', fontsize=17, fontweight='bold', ha='center', va='center', zorder=12)
ax.text(1020, 385, "+51.8 Runs Above Expectation", color='#94A3B8', fontsize=13, fontweight='bold', ha='center', va='center', zorder=12)

# #1 Bowler Box
ax.add_patch(patches.FancyBboxPatch((850, 135), 340, 200, boxstyle="round,pad=10", fc='#131E3A', ec='#3B82F6', lw=1.5, zorder=11))
ax.text(1020, 300, "TOP CLUTCH BOWLER", color='#38BDF8', fontsize=14, fontweight='heavy', ha='center', va='center', zorder=12)
ax.text(1020, 250, "MATHEESHA PATHIRANA", color='white', fontsize=19, fontweight='heavy', ha='center', va='center', zorder=12)
ax.text(1020, 200, "+43.6 Runs Saved (RSAE)", color='#F59E0B', fontsize=17, fontweight='bold', ha='center', va='center', zorder=12)
ax.text(1020, 160, "419 Pressure Balls Tested", color='#94A3B8', fontsize=13, fontweight='bold', ha='center', va='center', zorder=12)

plt.savefig(OUTPUT_PATH, dpi=100, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight', pad_inches=0)
plt.close()
print("Thumbnail generated successfully at:", OUTPUT_PATH)
