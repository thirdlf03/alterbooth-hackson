document.getElementById('post-button').addEventListener('click', function() {
    const content = document.getElementById('post-content').value;
    if (content.trim() !== '') {
        const post = document.createElement('div');
        post.className = 'post';
        post.textContent = content;
        document.getElementById('posts').appendChild(post);
        document.getElementById('post-content').value = '';
    }
});
