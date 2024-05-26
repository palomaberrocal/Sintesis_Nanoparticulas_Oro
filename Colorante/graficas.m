close all
clc
clear all

delimiter = '\t'; % Están separadas por tabulador
dataStartLine = 2; % Nos saltamos las cabeceras y cogemos los datos directamente
opts = delimitedTextImportOptions('DataLines', dataStartLine, 'Delimiter',delimiter);

myFolder = pwd;
filePattern = fullfile(myFolder, '*.txt');
files = dir(filePattern);
%filenames = {files.name};
filenames = {'106_PruebaPuntual_1E-5M.txt', '71_PruebaPuntual.txt', '110_PruebaPuntual50x.txt', '111_PruebaPuntual_1E-6M.txt', '113_MappingColorante10-7M_Acq12554.txt', '112_PruebaPuntual10-7M.txt'};

maximos = [];
maximos_ph = [];

figure
hold on
for i = 1:length(filenames)
    filename = filenames{i};
    data = readtable(filename, opts);
    
    onda = data{:,1}; 
    intensidad = data{:,2};

    % Cambiarlo a numero
    onda = str2double(onda');
    intensidad = str2double(intensidad');

    % Encontrar los valores de lambda 1050 y 1450
    n1 = 1050;
    [~, indice1]=min(abs(onda-n1));
    n2 = 1450;
    [~, indice2]=min(abs(onda-n2));

    onda = onda(1, indice1:indice2);
    intensidad = intensidad(1, indice1:indice2);
        
    if filename == "106_PruebaPuntual_1E-5M.txt" || filename == "110_PruebaPuntual50x.txt" || filename == "113_MappingColorante10-7M_Acq12554.txt" 
        maximos = [maximos max(intensidad)];
    else
        maximos_ph = [maximos_ph max(intensidad)];
    end

    plot(onda, intensidad)
    title('Lambda vs Intensidad')
    xlabel('{\lambda} nm.')
    ylabel('Intensidad')
    grid on
end

legendCell = {'10^{-5}M (estándar)', '10^{-5}M (pH 3,6)', '10^{-6}M (estándar)', '10^{-6}M (pH 3,6)', '10^{-7}M (estándar)', '10^{-7}M (pH 3,6)'};
legend(legendCell)

eje_x = [10^-5, 10^-6, 10^-7];
figure
hold on
plot(eje_x, maximos, '-o', 'MarkerSize',7)
plot(eje_x, maximos_ph, '-o', 'MarkerSize',7)
xlabel('Concentración (M)')
ylabel('Intensidad')
legend({'Estándar', 'pH 3,6'})







