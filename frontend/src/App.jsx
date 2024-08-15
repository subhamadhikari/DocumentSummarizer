import React,{useState} from 'react'
import MessageBox from './components/MessageBox'
import SessionCard from './components/SessionCard'
import SearchBar from './components/SearchBar'

const App = () => {

  const api = import.meta.env.VITE_BACKEND_URL;

  const [sidebar, setSidebar] = useState(true)
  const toggleSidebar = () => {
    setSidebar(!sidebar)
  }

  const user = {
    first_name:"subham",
    last_name:"adhikari",
    password:"asasa",
    email:"subham@gmail.com",
  }

  const testApi = async () => {
    const res = await fetch(`${api}/register`,{
      method:"POST",
      headers: {
        'Content-Type': 'application/json',
      },
      body:JSON.stringify(user)
    })

    const data = await res.json()
    console.log(data)
  }

  return (
    <main className='flex justify-center items-center'>
      {console.log(api+" ---> api url")}
        <div className={`leftPanel ${sidebar ? 'active' : 'inactive' }`}>
          <div className='flex justify-between items-center p-3'>
            <svg xmlns="http://www.w3.org/2000/svg" onClick={toggleSidebar} fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-8 transition-all hover:cursor-pointer">
              <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
            </svg>
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
              <path stroke-linecap="round" stroke-linejoin="round" d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10" />
            </svg>
          </div>
          <p className='w-full p-3 font-medium text-xl'>Chat Sessions</p>
          <div className='flex flex-col justify-start items-center p-2 h-[70vh] no-scrollbar overflow-auto'>
            <SessionCard/>
            <SessionCard/>
            <SessionCard/>
            <SessionCard/>
            <SessionCard/>
            <SessionCard/>
            <SessionCard/>
            <SessionCard/>
            <SessionCard/>
            <SessionCard/>
          </div>
        </div>
        <div className='rightPanel'>
            <div className='sticky flex justify-between items-center bg-rightPanel h-[10%] w-full'>
              <p className='font-bold text-xl flex justify-center items-center'>
                {
                  !sidebar && 
                  (
                    <svg xmlns="http://www.w3.org/2000/svg" onClick={toggleSidebar} fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="mx-1 size-8 rounded-full transition-all hover:cursor-pointer">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
                    </svg>
                  )
                }
                DocumentGPT
              </p>
              <div class="font-semibold text-xl flex items-center justify-center w-12 h-12 bg-purple-500 rounded-full text-white">
                A
              </div>
            </div>
            <div className='h-[80%] no-scrollbar overflow-auto p-10 bg-rightPanel'>
              <MessageBox text={'This is a human message. Hello! How are you? Give me all the details'}/>
              <MessageBox type={'ai'} text={'This is an ai message! Sorry I am unable to do so give correct text'}/>
              <MessageBox type={'ai'} text={'This is an ai message! Sorry I am unable to do so give correct text'}/>
              <MessageBox type={'human'} text={"This is a human message. Hello! How are you? Give me all the details"}/>
              <MessageBox type={'ai'} text={'This is an ai message! Sorry I am unable to do so give correct text'}/>
              <MessageBox type={'human'} text={"This is a human message. Hello! How are you? Give me all the details"}/>
              <MessageBox type={'ai'} text={'This is an ai message! Sorry I am unable to do so give correct text'}/>
              <MessageBox type={'human'} text={"This is a human message. Hello! How are you? Give me all the details"}/>
              {/* <button type='file'>Test</button> */}
            </div>
            <SearchBar/>
        </div>
    </main>
  )
}

export default App