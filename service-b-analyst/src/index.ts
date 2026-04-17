import express from 'express'
import {startConsumer} from './consumer'
import {initDb} from './db'
import router from './routes'

const app = express()
const PORT = 3001

app.use(express.json())
app.use(router)

app.get('/health', (req,res) => {
    res.json({status: 'ok'})
})

app.listen(PORT, async () => {
    console.log(`Service B running on port ${PORT}`)
    initDb()
    startConsumer().catch(console.error)
}) 

