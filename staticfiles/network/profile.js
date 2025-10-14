
document.addEventListener('DOMContentLoaded',()=> {
    const follow_button = document.querySelector('#follow-button');
    if (follow_button) {
    follow_button.addEventListener('click', ()=> togglefollow(follow_button))
    }
    const username = document.querySelector('h1').dataset.username;
    load_posts(`${username}`)
})

function togglefollow(button) {
    const profile_username = button.dataset.username;

    fetch(`/toggle_follow/${profile_username}/`,{
        method: 'PUT',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
        .then(response => response.json())
        .then(data => {
            console.log("follows?:", data.follow_status)
            if (data.follow_status === "followed") {
                button.textContent = "Unfollow";
                button.classList.remove('follow')
                button.classList.add('unfollow')
            } else if (data.follow_status==="unfollowed") {
                button.textContent = "Follow"
                button.classList.remove('unfollow')
                button.classList.add('follow')

            }

            // update follower count
            document.querySelector("#followers-count").textContent = data.follower_count;

        })


}