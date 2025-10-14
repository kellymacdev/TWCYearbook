// Django docs standard function to deal with csrf tokens
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function load_posts(profile_name, page = 1) {
        document.querySelector('#all-posts').innerHTML = "";
        fetch(`/posts/${profile_name}?page=${page}`)
            .then(response => response.json())
            .then(data => {
                console.log(`loading posts on page ${page}:`, data.posts);

                data.posts.forEach(post => {
                    const individual_post = document.createElement('div');
                    individual_post.id = `post-${post.id}`
                    individual_post.className = 'post';
                    individual_post.innerHTML = `<a class="username-display" href="/${post.user}">${post.user}</a><br>
                                                <br>
                                                <div class="contents-of-post">
                                            <p class="post-content">${post.content}</p>
                                            </div>
                                            <p class="timestamp">${post.timestamp}</p>
                                            <p><ion-icon name="heart" class="${post.liked ? 'liked' : ''}" data-post-id="${post.id}">
                                            </ion-icon> <span class="like-count">${post.likes}</span> </p> 
                                            `
                    if (post.my_post) {
                        individual_post.innerHTML += '<button class="edit-button">Edit post</button>';
                        const editButton = individual_post.querySelector('.edit-button');
                        editButton.addEventListener('click', ()=>edit_post(post.id))
                    }

                    document.querySelector('#all-posts').append(individual_post);

                    // like post function
                    const like_icon = individual_post.querySelector('ion-icon');
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
                                } else if (data.like_status==="unliked") {
                                    like_icon.classList.remove('liked')
                                }
                            // update like count
                            individual_post.querySelector(".like-count").innerHTML = data.like_count

                            })

                    })


                    // pagination
                    const current_page = data.page;
                    const total_pages = data.total_pages;
                    const has_next = data.has_next;
                    const has_previous = data.has_previous;

                    const pagination_nav = document.querySelector('.pagination');
                    pagination_nav.innerHTML = '';
                    const nav_list = document.createElement('ul');
                    nav_list.className='pagination justify-content-center mt-4';

                    if (has_previous) {
                        const previous = document.createElement('li');
                        previous.className = `page-item`;
                        previous.innerHTML = `<a class="page-link" href="#">Previous</a>`;
                        previous.addEventListener('click', () => load_posts(profile_name, page = current_page - 1));
                        nav_list.append(previous);
                    }

                    for (let i=1; i<=total_pages; i++) {
                        const page_list_item = document.createElement('li');
                        page_list_item.className = `page-item ${i === current_page ? 'active' : ''}`;
                        page_list_item.innerHTML = `<a class="page-link" href="#">${i}</a>`
                        page_list_item.addEventListener('click', ()=>load_posts(profile_name, page=i));
                        nav_list.append(page_list_item);
                    }

                    if (has_next) {
                        const next = document.createElement('li');
                        next.className = `page-item`;
                        next.innerHTML = `<a class="page-link" href="#">Next</a>`;
                        next.addEventListener('click', () => load_posts(profile_name, page = current_page + 1));
                        nav_list.append(next);
                    }

                    pagination_nav.append(nav_list);


                })
            })

}

function edit_post(post_id) {
    fetch(`/post/${post_id}`)
        .then(response => response.json())
        .then(post => {
            console.log("post from server:", post);

            const div_post_to_edit = document.querySelector(`#post-${post_id}`)
            div_post_to_edit.querySelector('.contents-of-post').innerHTML = `
                                            <form class="edit-content">
                                                <textarea class="edit-post-textarea">${post.content}</textarea><br>
                                                <input type="submit" value="Save post">
                                            </form>
                                            `
            const form = div_post_to_edit.querySelector('form');
            const textarea = form.querySelector('textarea');
            textarea.focus();
            textarea.setSelectionRange(textarea.value.length, textarea.value.length);
            form.addEventListener('submit', (event) => {
                event.preventDefault();
                console.log('you hit save')
                replace_content(post.id, form)
            })




        })

}

function replace_content(post_id, form) {
    const edited_content = form.querySelector('textarea').value;
    fetch(`/post/${post_id}`, {
       method: 'PUT',
       headers: {
               'X-CSRFToken': getCookie("csrftoken")
       },
       body: JSON.stringify({
           content: edited_content
            })
    })

        .then(response => response.json())
        .then(data => {
            console.log("new content back:", data.content);
            const post_to_edit = document.querySelector(`#post-${data.id}`)
            post_to_edit.querySelector('.contents-of-post').innerHTML = `<p class="post-content">${data.content}</p>`
        })

}


