import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] = ['Segoe UI Emoji', 'Arial']

def plot_probabilities(probs, team1, team2, save_path=None):
    """
    probs: [home_prob, draw_prob, away_prob]
    """
    labels = [f'🏠 {team1}', '🤝 Равен', f'✈️ {team2}']
    colors = ['#2ecc71', '#f39c12', '#e74c3c']
    plt.figure(figsize=(8, 5))
    bars = plt.bar(labels, probs, color=colors, edgecolor='black')
    plt.ylabel('Вероятност (%)')
    plt.title(f'Прогноза: {team1} срещу {team2}')
    plt.ylim(0, 100)
    for bar, prob in zip(bars, probs):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                 f'{prob:.1f}%', ha='center', fontweight='bold')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    if save_path:
        plt.savefig(save_path, dpi=100, bbox_inches='tight')
        print(f"📊 Графиката е запазена в {save_path}")
    plt.close()


def plot_feature_importance(importance_dict, save_path=None):
    """
    importance_dict: {feature_name: importance}
    """
    sorted_items = sorted(importance_dict.items(), key=lambda x: x[1], reverse=True)
    names = [item[0] for item in sorted_items]
    values = [item[1] for item in sorted_items]
    plt.figure(figsize=(10, 6))
    plt.barh(names, values, color='#3498db')
    plt.xlabel('Важност')
    plt.title('Важност на характеристиките (Feature Importance)')
    plt.gca().invert_yaxis()
    if save_path:
        plt.savefig(save_path, dpi=100, bbox_inches='tight')
        print(f"📊 Feature importance saved to {save_path}")
    plt.close()
