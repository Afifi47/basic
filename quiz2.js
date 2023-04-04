let dbUsers = [
    {
        username: "Ipi",
        password: "767343",
        name: "Afifi",
        email: "afifiasri007@gmail.com"
    };
    {
        username: "Tadak",
        password: "197000",
        name: "Harith",
        email: "tadakikun@gmail.com"
    },
    {
        username: "Anep",
        password: "999999",
        name: "Haniff",
        email: "haniff@gmail.com"
    }
]

function login(reqUsername, reqPassword){
    let matchUser = dbUsers.find(
        user => user.username == reqUsername
    )
    console.log(matchUser)
}
// try to login
login("Afifi", "password")