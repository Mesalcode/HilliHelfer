const CharacterAI = require('node_characterai');
const characterAI = new CharacterAI();

const express = require('express');
const app = express();
app.use(express.json()) ;


(async() => {

        try {
            await characterAI.authenticateAsGuest();

            const characterId = "HC05wmFsL7QVaaE4FTu1fayTkZHo4l7AjzEL5KKDWJE" // Discord moderator
        
            let chat = await characterAI.createOrContinueChat(characterId);        

            app.get('/status', (req, res) => res.send('Up!'))

            app.post('/get_response', async (req, res) => {
                query = req.body.query;
        
                for (let i = 0; i < 3; i++) {
                    try {
                        if (i > 0) {
                            characterAI.unauthenticate()
                            await characterAI.authenticateAsGuest()
    
                            chat = await characterAI.createOrContinueChat(characterId);  
                        }

                        const response = await chat.sendAndAwaitResponse(query, true);
            
                        return res.send(response.text)
                    } catch (_) {
                        console.log(_)
                    }

                    await new Promise(resolve => setTimeout(resolve, 3000))
                }

                return res.send('Entschuldige. Das habe ich nicht verstanden.')
            })

            app.listen(3002, () => {});
        } catch (_) {
            console.log(_)
        }
    
})();