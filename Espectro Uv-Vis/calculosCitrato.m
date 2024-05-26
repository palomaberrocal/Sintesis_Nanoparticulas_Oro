close all
clc
clear all

delimiter = '\t'; % Están separadas por tabulador
dataStartLine = 3; % Nos saltamos las cabeceras y cogemos los datos directamente
opts = delimitedTextImportOptions('DataLines', dataStartLine, 'Delimiter',delimiter);

myFolder = pwd;

all_files = dir;
all_dir = all_files([all_files(:).isdir]);
num_dir = numel(all_dir)-2;

for i = 1:num_dir
    myFolder = [pwd, '\', num2str(i)];
    filePattern = fullfile(myFolder, '*.txt');
    files = dir(filePattern);
    filenames = {files.name};

    for j = 1:length(filenames)
        filename = filenames{j};
        if strcmp(filename,'ambos.txt') == 1
            continue
        else
            data = readtable([myFolder, '\', filename], opts);
        
            lambda1 = data{:,1}; 
            abs1 = data{:,2};
        
            % Hay que cambiar , por .
            lambda1 = strrep(lambda1, ',', '.');
            abs1 = strrep(abs1, ',', '.');
        
            % Cambiarlo a numero
            lambda1 = str2double(lambda1');
            abs1 = str2double(abs1');
        
            % Encontrar los valores de lambda 300 y 800
            n1 = 300;
            [~, indice1]=min(abs(lambda1-n1));
            n2 = 800;
            [~, indice2]=min(abs(lambda1-n2));

            lambda1 = lambda1(1, indice1:indice2);
            abs1 = abs1(1, indice1:indice2);
            
            lambda_data{i,j} = lambda1;
            abs_data{i,j} = abs1;
        
            leyenda{i,j} = strrep(filename, '.txt', '');
        end
    end
end

[length1, width1] = size(lambda_data);
index_num = length(lambda1);
lambda_means = cell(length1, 1);
abs_means = cell(length1, 1);
legend_index = cell(length1, 1);
legend_means = cell(length1, 1);

for i = 1:length1
    for k = 1:index_num
        lambda_index=cell(length1, 1);
        abs_index=cell(length1, 1);
        for j = 1:width1
            lambda_index{i,1} = [lambda_index{i,1} lambda_data{i,j}(k)];
            abs_index{i,1} = [abs_index{i,1} abs_data{i,j}(k)];
        end
        lambda_means{i,1} = [lambda_means{i, 1} mean(lambda_index{i,1})];
        abs_means{i,1} = [abs_means{i, 1} mean(abs_index{i,1})];
    end
end

for i = 1:length1
    for j = 1:width1
        legend_index{i, 1} = [legend_index{i, 1} (str2double(leyenda{i,j}))];
    end
    media = mean(legend_index{i,1});
    legend_means{i,1} = [sprintf('%.2e', media)];
end

figure
hold on
for i = 1:length1
    plot(lambda_means{i,1}, abs_means{i,1})
    title('Variación de la variación de oro vs Extinción')
    xlabel('λ (nm)')
    ylabel('Extinción')
    grid on
end
legend(legend_means)



