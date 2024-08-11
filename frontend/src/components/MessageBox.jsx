import React from 'react'

const MessageBox = ({type,text}) => {
  return (
    <>
    {
        (type=="ai") ?
        (
        <div className='bg-message-box-ai p-3 max-w-sm rounded-e-xl rounded-es-xl mb-3'>
            <p>{text}</p>
        </div>
        ):
        (
        <div className='bg-message-box-human p-3 max-w-sm rounded-s-xl rounded-b-xl rounded--xl mb-3 ml-auto'>
            <p>{text}</p>
        </div>
        )
    }


    </>
  )
}

export default MessageBox