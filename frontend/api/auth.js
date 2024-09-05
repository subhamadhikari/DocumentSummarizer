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
