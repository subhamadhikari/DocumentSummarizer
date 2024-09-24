const api = import.meta.env.VITE_BACKEND_URL;

const getToken = () => {
    const token = localStorage.getItem("token")
    return token
}

export const submitDocument = async (URL,file) => {
    const url = URL+"/startchat"
    const formData = new FormData();
    formData.append('document',file)

    const response = await fetch(url,{
        method:"POST",
        body:formData
    })

    const data = await response.json()
    console.log(data)
}

export const chatAI = async (URL,text) => {
    const url = URL+"/mychat"

    const response = await fetch(url,{
        method:"POST",
        headers:{
        'Accept': 'application/json',
          "Content-Type":"application/json"  
        },
        body:JSON.stringify({"question":text})
    })

    const data = await response.json()
    const res = JSON.stringify(data.result)
    console.log(res)
    return res
}

export const loadChat = async() =>{
    const token = getToken()
    const url = api + "/loadchatlist"
    const response = await fetch(url,{
       method:"GET",
       headers:{
        "Authorization":`Bearer ${token}`
    }
    })
    if (response.ok) {
        const data = await response.json()
        console.log(data)
        return data        
    }
    console.log(response,"loadChat ====>> response")

}

export const loadPreviousChat = async(session) => {
    const url = api + `/loadchat?chat_session=${session}`
    const token = getToken()
    const response = await fetch(url,{
        method:"GET",
        headers:{
            "Authorization":`Bearer ${token}`
        }
    })
    const data = await response.json()
    return data
}

