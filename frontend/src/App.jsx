import React from 'react'
import MessageBox from './components/MessageBox'

const App = () => {
  return (
    <main className='flex justify-center items-center'>
        <div className='leftPanel'>
            <p className='w-1'>Left Panel</p>
        </div>
        <div className='rightPanel'>
            <div className='sticky flex justify-between items-center bg-rightPanel h-[10%] w-full'>
              <p className='font-bold text-xl'>DocumentGPT</p>
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
            </div>
            <div className=' h-[10%] flex justify-center items-center'>
                <input type='text' placeholder='What do you want to ask me?' className='focus:ring-2 focus:ring-blue-500 focus:outline-none w-1/2 leading-6 text-slate-50 placeholder-slate-400 py-2 pl-10 ring-1 ring-slate-200 shadow-sm rounded-full p-2 bg-text-box'/>
            </div>
        </div>
    </main>
  )
}

export default App