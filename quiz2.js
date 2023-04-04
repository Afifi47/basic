let dbUsers = [
    {
        username: "Ipi",
        password: "767343",
        name: "Afifi",
        email: "afifiasri007@gmail.com"
    },
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
    if(!matchUser) return "User not found!"
    if(matchUser.password==reqPassword){
        return matchUser
    }else{
        return "invalid password"
    }

}

function register(reqUsername,reqPassword,reqName,reqEmail){
    dbUsers.push({
        username: reqUsername,
        password: reqPassword,
        name: reqName,
        email: reqEmail
    })
}
// try to login
console.log(login("Ipi", "767343"))
console.log(login("Afifi", "767343"))
console.log(login("Anep", "999999"))

register("Penyu","123456","Amir","penyu@gmail.com")
console.log(login("Penyu","123456"))