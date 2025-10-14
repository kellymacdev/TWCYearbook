document.addEventListener('DOMContentLoaded',()=> {
    load_posts('all');

    document.querySelector('#new-post-content').value = "";

    document.querySelector('#new-post-form').onsubmit = event => newPost(event)

})

function newPost(event) {
        event.preventDefault();
        const new_post_content = document.querySelector('#new-post-content').value;

        fetch('/posts/blank', {
                method: 'POST',
                body: JSON.stringify({new_post_content}),
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                }
            }
        )
            .then(response => response.json())
            .then(post => {
                console.log("new post:", post.content);
                const new_post = document.createElement('div')
                new_post.className = 'post';
                new_post.innerHTML = `<a class="username-display" href="/${post.user}">${post.user}</a> <br>
                                        <br>
                                         <div class="contents-of-post">
                                      <p>${post.content}</p>
                                      </div>
                                      <p class="timestamp">${post.timestamp}</p>
                                      <p><ion-icon name="heart" class="${post.liked ? 'liked' : ''}" data-post-id="${post.id}">
                                            </ion-icon> <span class="like-count">${post.likes}</span> </p>  `

                document.querySelector('#all-posts').prepend(new_post);
                document.querySelector('#new-post-content').value = "";

                const like_icon = new_post.querySelector('ion-icon');

                like_icon.addEventListener('click', () => {
                    console.log('clicked like on post:', like_icon.dataset.postId);
                    const post_id = like_icon.dataset.postId;

                    fetch(`/toggle_like/${post_id}/`, {
                        method: 'PUT',
                        headers: {
                                'X-CSRFToken': getCookie("csrftoken")
                        }
                    })
                        .then(response => response.json())
                            .then(data => {
                                console.log("likes?:", data.like_status);
                                if (data.like_status === "like") {

                                    like_icon.classList.add('liked')

                                } else if (data.like_status === "unliked") {

                                    like_icon.classList.remove('liked')

                                }
                                // update like count
                                new_post.querySelector(".like-count").innerHTML = data.like_count
                            })


                    })
            })

}



