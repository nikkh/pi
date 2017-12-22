using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System.Web;
using System.Web.Mvc;
using Microsoft.Azure;
using Microsoft.Azure.KeyVault;
using Microsoft.IdentityModel.Clients.ActiveDirectory;

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