import { Router } from 'express'
import {getPokemon, getLeaderboard} from './db'

const router = Router()

router.get('/pokemon/:name', (req, res) => {
    const pokemon = getPokemon(req.params.name.toLowerCase())

    if(!pokemon) {
        res.status(404).json({error: `Pokemon ${req.params.name} not found`})
        return
    }

    res.json(pokemon)
})

router.get('/leaderboard', (req, res) => {
    const leaderboard = getLeaderboard()
    res.json(leaderboard)
})

export default router