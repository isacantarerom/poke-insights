import amqp from 'amqplib'
import { savePokemon } from './db'

const RABBITMQ_URL = process.env.RABBITMQ_URL || 'amqp://user:password@localhost:5672'
const QUEUE_NAME = 'pokemon.collected'

export async function startConsumer() {
    const connection = await amqp.connect(RABBITMQ_URL)
    const channel = await connection.createChannel()

    await channel.assertQueue(QUEUE_NAME, { durable: true })
    channel.prefetch(1)

    console.log(`[${new Date().toISOString()}] INFO: Waiting for messages in queue: ${QUEUE_NAME}`)

    channel.consume(QUEUE_NAME, (msg) => {
        if(msg == null) return
        
        try {
            const data = JSON.parse(msg.content.toString())
            console.log(`Received pokemon: ${data.name} | battle power: ${data.battle_power}`)
            
            savePokemon(data)
            console.log(`Saved ${data.name} to database`)
            
            channel.ack(msg)
        } catch (err) {
            console.error(`[${new Date().toISOString()}] ERROR: ailed to process message: ${err}`)
            channel.nack(msg, false, false)
        }

    })

}