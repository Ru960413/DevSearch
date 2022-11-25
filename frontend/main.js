let loginBtn = document.getElementById("login-btn")
let logoutBtn = document.getElementById("logout-btn")

let token = localStorage.getItem("token")

// if we are logged in then remove the login button
if(token){
    loginBtn.remove()
}
// else remove the logout button
else{
    logoutBtn.remove()
}
// if logout button is clicked then remove the token from local storage
logoutBtn.addEventListener("click", (e) => {
    e.preventDefault()
    localStorage.removeItem("token")
    window.location = "file:///Users/Hu/Desktop/frontend/login.html"
})


let projectsURL = "http://127.0.0.1:8000/api/projects/"

let getProjects = () => {
    
    //get response from the URL and convert it into JSON object
    fetch(projectsURL)
    .then(response => response.json())
    //show the data in console
    .then(data => {
        console.log(data)
        buildProjects(data)
    })
}


let buildProjects = (projects) => {
    let projectWrapper = document.getElementById("projects--wrapper")
    projectWrapper.innerHTML = ""
    for (let i = 0; projects.length > i; i++){
        let project = projects[i]
        
        let projectCard = `
            <div class="project--card">
                <img src="http://127.0.0.1:8000${project.feature_image}" />
                
                <div>
                    <div class="card--header">
                        <h3>${project.title}</h3>
                        <strong class="vote--option" data-vote="up" data-project="${project.id}">&#43;</strong>
                        <strong class="vote--option" data-vote="down" data-project="${project.id}">&#8722;</strong>
                    </div>
                    <i>${project.vote_ratio}% Positive feedback</i>
                    <p>${project.description.substring(0,150)}</p>
                </div>
            </div>
        `
        projectWrapper.innerHTML += projectCard

    }

    //Add event listener
    addVoteEvents()
}

let addVoteEvents = () => {
    let voteBtns = document.getElementsByClassName("vote--option")
    for (let i=0; i < voteBtns.length; i++){
        voteBtns[i].addEventListener("click", (e)=>{
            let token = localStorage.getItem("token")
            console.log("token:", token)

            let vote = e.target.dataset.vote
            let project = e.target.dataset.project
            // console.log("PROJECT:", project, "VOTE:", vote)
            fetch(`http://127.0.0.1:8000/api/projects/${project}/vote/`, {
                method:"POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization:`Bearer ${token}`
                },
                body:JSON.stringify({"value": vote})
            })
            .then(response=>response.json())
            .then(data => {
                console.log("SUCCESS:", data)
                getProjects()

            })
        })
    }
}

getProjects()