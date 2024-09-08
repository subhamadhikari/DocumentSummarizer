const api = import.meta.env.VITE_BACKEND_URL;

const getToken = () => {
    const token = localStorage.getItem("token")
    return token
}

export const getCurrentUser = async() => {
    const token = getToken()
    const url = api+"/getCurrentUser"
    const response = await fetch(url,{
        method:"GET",
        headers:{
            "Authorization":`Bearer ${token}`
        }
    })

    const data = await response.json()
    console.log("after authorization::",data)
    console.log("after authorization -- email::",data.email)
    return data.email
}