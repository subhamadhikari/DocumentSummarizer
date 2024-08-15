

export const submitDocument = async (URL,file) => {
    const url = URL+"/submitdocument"
    const formData = new FormData();
    formData.append('document',file)

    const response = await fetch(url,{
        method:"POST",
        body:formData
    })

    const data = await response.json()
    console.log(data)
}