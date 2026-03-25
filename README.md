##Docker Optimization
Placing requirements.txt before copying the rest of the source code allows Docker to cache the dependency installation layer. This means that if only the application code changes but dependencies remain the same, Docker will reuse the cached layer and skip reinstalling packages, As a result, build times become significantly faster.


 IMAGE          CREATED          CREATED BY                                      SIZE      COMMENT
438842a2428f   18 minutes ago   /bin/sh -c #(nop)  CMD ["python" "bot.py"]      0B        
618b2de913dd   18 minutes ago   /bin/sh -c #(nop)  EXPOSE 8000                  0B        
62bfe04eafa6   18 minutes ago   /bin/sh -c #(nop)  ENV PORT=8000                0B        
2a365c200d2c   18 minutes ago   /bin/sh -c #(nop) COPY dir:608ff5c5700877535…   7.2kB          
