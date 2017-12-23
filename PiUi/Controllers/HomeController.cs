using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System.Web;
using System.Web.Mvc;
using Microsoft.Azure;
using Microsoft.Azure.KeyVault;
using Microsoft.WindowsAzure.Storage; // Namespace for CloudStorageAccount
using Microsoft.WindowsAzure.Storage.Queue; // Namespace for Queue storage types
using Microsoft.IdentityModel.Clients.ActiveDirectory;
using Microsoft.WindowsAzure.Storage.Blob;

namespace PiUi.Controllers
{
    public class HomeController : Controller
    {
       
        public ActionResult Index()
        {
            var kv = new KeyVaultClient(new KeyVaultClient.AuthenticationCallback(PiUiUtil.GetTokenForCurrentApplication));
            string piStorageAccountName = kv.GetSecretAsync(CloudConfigurationManager.GetSetting("piStorageAccountName_KvUri")).Result.Value;
            string piStorageAccountSecretKey = kv.GetSecretAsync(CloudConfigurationManager.GetSetting("piStorageAccountSecretKey_KvUri")).Result.Value;
            string piStorageAccountCameraContainerName = kv.GetSecretAsync(CloudConfigurationManager.GetSetting("piStorageAccountCameraContainerName_KvUri")).Result.Value;
            string piStorageAccountCameraStillImagesQueueName = kv.GetSecretAsync(CloudConfigurationManager.GetSetting("piStorageAccountCameraStillImagesQueueName_KvUri")).Result.Value;
            string storageConnection = String.Format("DefaultEndpointsProtocol=https;AccountName={0};AccountKey={1}", piStorageAccountName, piStorageAccountSecretKey);
            CloudStorageAccount storageAccount = CloudStorageAccount.Parse(storageConnection);
            CloudQueueClient queueClient = storageAccount.CreateCloudQueueClient();
            
            CloudQueue queue = queueClient.GetQueueReference(piStorageAccountCameraStillImagesQueueName);
            queue.EncodeMessage = true;
            // Peek at the next message
            CloudQueueMessage message = queue.GetMessage();
            

            // Display message.
            Console.WriteLine();

            // Create the blob client.
            CloudBlobClient blobClient = storageAccount.CreateCloudBlobClient();

            // Retrieve reference to a previously created container.
            CloudBlobContainer container = blobClient.GetContainerReference(piStorageAccountCameraContainerName);

            // Retrieve reference to a blob ie "picture.jpg".
            CloudBlockBlob blockBlob = container.GetBlockBlobReference(message.AsString);
            //------

            var newUri = new Uri(blockBlob.Uri.AbsoluteUri);

            ViewBag.ImageUri = newUri;


            return View();
        }

        public ActionResult About()
        {
            ViewBag.Message = "Your application description page.";

            return View();
        }

        public ActionResult Contact()
        {
            ViewBag.Message = "Your contact page.";

            return View();
        }
    }
}