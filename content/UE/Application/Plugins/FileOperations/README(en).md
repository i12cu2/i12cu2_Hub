# Unreal Engine Blue Prints Library Node


UE 5.8.2

<details>
<summary>API parsing (English)</summary>
<pre><code>

static FString ReadStringToFile(FString Dir)
Function:
Reading a file
Input:
FString Dir: The file path
Output:
FString Result: The file contents

static void WriteStringToFile(FString FileName, FString content) {
Function:
Write to file wide character UTF-16
Input:
FString FileName: The file path
FString content: The file content

static bool WriteStringToFileU8(FString FileName, FString content)
Function:
Write to the file UTF-8
Input:
FString FileName: The file path
FString content: The file content
Output:
bool ver: Whether the write was successful

static TArray<FString> FindFilesTo(FString Path, FString Filter, bool Files,bool Directory)
Function:
Finding files
Input:
FString Path: File directory path
FString Filter: Filename filter
bool Files: Whether to look for files
Output:
TArray<FString> ver: All file paths in the file directory

static bool MoveFileTo(FString To, FString From)
Funtionc:
Moving files
Input:
FString To: The destination file path
FString From: The source file path
Output:
bool ver: Whether the move was successful

static int32 CopyFileTo(FString To, FString From)
Function:
Copying files
Input:
FString To: The destination file path
FString From: The source file path

static bool DeleteFileTo(FString FilePath)
Function:
Deleting files
Input:
FString FilePath: The file path

static void OpenFile(FString FilePath)
Function:
Opening a file
Input:
FString FilePath: The file path

static void CreateDic(FString filePath)
Function:
Creating folders
Input:
FString filePath: The file path

static void DeleteDic(FString filePath)
Function:
Deleting folders
Input:
FString filePath: The file path

static int64 GitFileSize(FString filePath)
Function:
Getting the file size
Input:
FString filePath: The file path
Output:
int64 ver: The file size

static TArray<FString> FindFolder(FString Path, FString Filter, bool Files,bool Directory)
Funtcion:
Find all files in the file directory
Input:
FString Path: File directory path
FString Filter: Filename filter
bool Files: Whether to look for files
bool Directory: Whether to look for folders
Output:
TArray<FString> ver: All file paths in the file directory

static TArray<FString> GetFolderFiles(FString Path)
Function:
Search all files in the file directory, cannot delete search
Input:
FString Path: File directory path
Output:
TArray<FString> ver: All file paths in the file directory

static void CopyMessageToClipboard(FString text)
Function:
Overwrite the clipboard contents
Input:
FString text: Copies the content

static FString PasteMessageFromClipboard()
Function:
Gets the clipboard contents
Output:
FString ver: The output

static bool IsValidFilePath(const FString& FilePath)
Function:
Determines if the path is valid
Input:
FString& FilePath: The file path
Output:
bool ver: Whether the path is valid

static TArray<FString> GetFilesInDirectory(const FString& DirectoryPath)
Function:
To get a file with a specified path, you can only get a folder
Input:
FString& DirectoryPath: Folder path
Output:
TArray<FString> ver: path to the folder file

static TArray<FString> GetMP3FilePaths(const FString& Directory)
Function:
Only mp3 files can be retrieved from the specified path
Input:
FString& Directory: Folder path
Output:
TArray<FString> ver: path to the folder file

static FString GetFileNameFromPath(const FString& FilePath)
Function:
Extract the filename from the file path
Input:
FString& FilePath: The file path
Output:
FString ver: Filename

static bool DeleteFileAtPath(const FString& FilePath)
Function:
Deleting files
Input:
FString& FilePath: The file path
Output:
bool ver: Whether the operation was successful

static float SetSUVM()
Function:
UE can play in the background
Output:
float ver: Output 1.0f for background playback,0.0f for non-background playback

static bool SaveConstraintArray(FString SaveDirectory, FString Filename, TArray<FString> SaveText,  bool AllowOverWriting);
Function:
The exported array data is saved locally
Input:
FString SaveDirectory: Save to the destination path
FString Filename: This specifies the name of the exported csv file
TArray<FString> SaveText: Stores content separated by "," as columns and array index as rows
bool AllowOverWriting: Whether to override
Output:
bool ver: Whether the export was successful

static TArray<FString> LoadConstraintArray(FString FilePath);
Function:
Import the array data into the blueprint
Input:
FString FilePath: The path to read the csv
Output:
TArray<FString> ver: This returns the contents of the csv

static bool DeleteFile(FString FilePath);
Function:
Delete specified file
Input:
FString FilePath: The path to delete the target file
Output:
bool ver: Whether the deletion was successful

static TArray<ULineBatchComponent*> DrawRayLine(FVector StartPos, FVector EndPos, float fLifeTime, FLinearColor color);
Function:
Draw a line
Input:
FVector StartPos: The 3D starting point of the line
FVector EndPos: The 3D end of the line
float fLifeTime: The lifetime of the drawn line (about 0.02s recommended)
FLinearColor color: The color of the drawing line
Output:
TArray<ULineBatchComponent*> ver: The object on which the line is drawn

static void DestoryLine(TArray<ULineBatchComponent*> LineList);
Function:
The object that clears the line object
Input:
TArray<ULineBatchComponent*> LineList: The line object to be cleared

static TArray<FString> GetAllSaveFileNames(const FString& Directory);
Function:
Gets a list of files in the file path
Input:
FString Directory: The path to the root directory of the file
Output:
TArray<FString> ver: File object path group under path

static FString GetFileNamePath(const FString& FilePath)
Function:
Get the texture (image) from the file path and create the returned object
Input:
FString FilePath: The path to the file
Output:
FString: Filename

static UTexture2D* LoadImageFromAbsolutePath(const FString& AbsolutePath);
Function:
Get the texture (image) from the file path and create the returned object
Input:
FString AbsolutePath: The path to the file
Output:
UTexture2D: Texture object pointer

static AActor* GetActorByName(TArray<AActor*> Actors, const FString& ActorName)
Function:
Actors are extracted according to UAID
Input:
TArray<AActor*> Actors :Actor search source
FString& ActorName :Actor name (UAID)
Output:
AActor* : The Actor pointer

static UMediaSource* LoadMediaSourceFromAbsolutePath(const FString& AbsolutePath)
Function:
Getting the media player
Input:
FString& AbsolutePath: The file path
Output:
UMediaSource: The media player pointer

</code></pre>
</details>