// Helper to create quick menu buttons
const addButton = (name) => {
    const newButton = document.createElement('button')
    newButton.innerText = name
    newButton.addEventListener('click', () => print(name))
    document.querySelector('.names').appendChild(newButton)
}

// Set up string and button for custom input
document.querySelector('.custom').addEventListener('submit', (event) => {
    event.preventDefault()

    // Get and reset input
    const custom = document.querySelector('.custom input').value
    document.querySelector('.custom input').value = ''

    // Send off to print
    print(custom)

    // If missing, create quick menu button
    if(!names.includes(custom)) {
        names.push(custom)
        addButton(custom)
    }
})

// Create quick menu buttons
const names = ['public', 'alice', 'bob']
names.map((name) => addButton(name))

// Handle clicks: send name and timestamp to printer
const print = async function (name) {
    showResponse('waiting', 'waiting for printer')
    console.log(name)

    try {
        const now = new Date
        const payload = { name: name, timestamp: `${now.toLocaleDateString('de-AT')} ${now.toLocaleTimeString('de-AT')}` }
        console.log(payload)
        const response = await fetch('/print', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload),
        })
        if (!response.ok) {
            throw new Error(`Response status: ${response.status}`)
        }

        const json = await response.json()
        if (json.status != 'success') {
            throw new Error(`JSON status: ${response.status}`)
        }
        success()
    } catch (error) {
        fail(error.message)
    }
}

// Inform user about success
const success = () => {
    console.log('success')
    showResponse('success', 'printed, yay!')
    setTimeout(hideResponse, 3000)
}

// Inform user about failure
const fail = (message) => {
    console.log(message)
    showResponse('error', message)
    setTimeout(hideResponse, 3000)
}

// Show response overlay
const showResponse = (type, message) => {
    const main = document.querySelector('main')
    const response = document.querySelector('div.response')

    response.className = `response ${type}`
    response.querySelector('p').innerText = message

    main.setAttribute('style', 'display: none')
    response.setAttribute('style', 'display: flex')
}

// Hide response overlay
const hideResponse = () => {
    document.querySelector('main').removeAttribute('style')
    document.querySelector('div.response').removeAttribute('style')  
}

// Handle overlay button
const closeButton = document.querySelector('div.response button')
closeButton.addEventListener('click', hideResponse)
