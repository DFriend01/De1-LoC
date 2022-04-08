const express = require('Express')

const app = express()
const port = 5000

app.get('/', (req,res)=>{
    res.send('Hello World!')
})

app.listen(port, ()=>{
    console.log(`Test server listening on port ${port}`)
})

