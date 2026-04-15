import express from 'express'
import {startConsumer} from './consumer'
import { start } from 'node:repl'

const app = express()
const PORT = 3001

app.use(express.json())

app.get('/health', (req,res) => {
    res.json({status: 'ok'})
})

app.listen(PORT, () => {
    console.log(`Service B running on port ${PORT}`)
    startConsumer().catch(console.error)
}) 

