import React,{useState} from 'react'

const SessionCard = () => {
    const [dropdown, setDropdown] = useState(false)

    const toggleDropdown = () => {
        setDropdown(!dropdown)
    }


  return (
    <div className='relative w-full p-4 bg-gray-800 border-gray-700 rounded-lg shadow hover:bg-gray-700 flex justify-between items-center mb-2'>
        <p className='truncate w-4/5'>Previous Chat</p>
        <div class="flex justify-end">
        <button id="dropdownButton" onClick={toggleDropdown} data-dropdown-toggle="dropdown" class="inline-block text-gray-400 hover:bg-gray-700 focus:ring-4 focus:outline-none focus:ring-gray-700 rounded-lg text-sm p-1.5" type="button">
            <span class="sr-only">Open dropdown</span>
            <svg class="w-5 h-5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 16 3">
                <path d="M2 0a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3Zm6.041 0a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3ZM14 0a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3Z"/>
            </svg>
        </button>
        {
            dropdown &&
            (
            <div id="dropdown" class="z-10 absolute top-12 left-4 text-base list-none divide-y divide-gray-100 rounded-lg shadow w-44 bg-[#2c3e50]">
                <ul aria-labelledby="dropdownButton">
                <li>
                    <a href="#" class="block px-4 py-2 text-sm  hover:bg-gray-600 text-gray-200 hover:text-white">Delete</a>
                </li>
                </ul>
            </div>
            )
        }
    </div>
    </div>
  )
}

export default SessionCard