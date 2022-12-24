O objetivo deste trabalho é aplicar filtragens no domínio da frequência para restaurar imagens que foram danificadas por ruídos altamente estruturados. Foram duas imagens (parthenon e eiffel) e dois ruídos (waves e tartan) nas quatro combinações.

Para fazer as filtragens de forma interativa, primeiro produza a máscara com o valor da magnitude das frequências da FFT das imagens:

Por exemplo:

python filter-fft.py parthenon-waves.png --output_fft_mask parthenon-waves-mask.png

Na sequência, você deve editar a máscara (no caso parthenon-waves-mask.png) pintando de vermelho (com uma ferramenta do tipo Paint ou GIMP) as regiões em que você deseja remover as frequências (nessas regiões o valor da transformada será zerado).

A seguir aplique sua máscara à imagem, por exemplo:

python filter-fft.py parthenon-waves.png --input_fft_mask parthenon-waves-mask.png --output_fft_result parthenon-waves-result.png

Examine o arquivo de saída (parthenon-waves-result.png) para verificar se está feliz com os resultados. Caso contrário, você pode continuar refinando a máscara. Você também pode comparar entre si as máscaras das quatro imagens para tentar diferenciar o sinal do ruído. O divertido dessa tarefa é conseguir fazer a restauração tão bem quanto possível SEM ter as imagens de referência para se guiar, como acontece na vida real.

A entrega serão as máscaras e os resultados para as quatro imagens, obrigatoriamente com os nomes abaixo:

eiffel-tartan-mask.png
eiffel-waves-mask.png
parthenon-tartan-mask.png
parthenon-waves-mask.png
eiffel-tartan-result.png
eiffel-waves-result.png
parthenon-tartan-result.png
parthenon-waves-result.png

Eu farei ao final uma comparação do quanto os resultados de cada grupo se aproximaram das imagens de referência em termos da distância quadrática média.
