document.addEventListener('DOMContentLoaded', () => {
    const rankingData = [
        { rank: 1, name: 'Alice', score: 100 },
        { rank: 2, name: 'Bob', score: 90 },
        { rank: 3, name: 'Charlie', score: 80 },
        // 追加のデータをここに挿入
    ];

    const tbody = document.querySelector('#ranking-table tbody');

    rankingData.forEach(data => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${data.rank}</td>
            <td>${data.name}</td>
            <td>${data.score}</td>
        `;
        tbody.appendChild(row);
    });
});