const api = import.meta.env.VITE_BACKEND_URL;

export const signup = async(user) => {
    const url = api + "/signup"
    const response = await fetch(url,{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify(user)
    })

    const data = await response.json()
    return data
}

export const signin = async(user) =>{

    const url = api + "/login"
    const formData = new FormData()
    formData.append("username",user.email)
    formData.append("password",user.password)

    const response = await fetch(url,{
        method:"POST",
        body:formData
    })

    console.log("above data",response)
    if(!response.ok){
        const data = await response.json()
        return {
            status_code:response.status,
            detail:data.detail
        }
    }
    const data = await response.json()
    // console.log("after login::",data)

    if(data.access_token){
        localStorage.setItem("token",data.access_token)
    }
    return data
}

