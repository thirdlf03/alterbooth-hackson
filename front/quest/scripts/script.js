document.addEventListener('DOMContentLoaded', () => {
    const questListItems = document.querySelectorAll('#quest-list li');
    const questDetailsSection = document.getElementById('quest-details');
    const questDescription = document.getElementById('quest-description');
    const startQuestButton = document.getElementById('start-quest');

    questListItems.forEach(item => {
        item.addEventListener('click', () => {
            const questText = item.textContent;
            questDescription.textContent = `${questText}の詳細がここに表示されます。`;
            questDetailsSection.style.display = 'block';

            // クエスト達成時の処理
            item.classList.toggle('completed');
        });
    });

    startQuestButton.addEventListener('click', () => {
        alert('クエストを開始します！');
    });
});