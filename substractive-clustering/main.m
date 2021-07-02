files = dir('*.dat'); 
fileID = fopen('exp.txt','a+');
for file = files'
    curFile = load(file.name);
    C = subclust(curFile,0.5);
    fprintf(fileID, 'project: %s cluster size: %d \n', file.name, length(C));
end
fclose(fileID);